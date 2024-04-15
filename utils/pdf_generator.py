from PIL import Image, ImageDraw

from django.http import HttpResponse
from django.views.generic import DetailView

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle


pdfmetrics.registerFont(TTFont('Calibri', 'media/fonts/calibri.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Bold', 'media/fonts/calibrib.ttf'))
custom_color_EN = colors.Color(0.125, 0.404, 0.325)
custom_color_EN_cropped = (32, 103, 83)
custom_color_DE = colors.Color(0.3215, 0.26666, 0.419607)
custom_color_DE_cropped = (82, 68, 107)


def crop_circular(image_path, output_path, color):
    image = Image.open(image_path)
    image = image.resize((400, 400))
    center = (200, 200)

    radius = 195  # Example radius
    # color = (32, 103, 83)

    # Create a circular mask
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=255)

    # Apply the mask to the image
    image.putalpha(mask)

    # Create a new image with the specified color
    cropped_image = Image.new('RGB', image.size, color)

    # Paste the masked image onto the colored image
    cropped_image.paste(image, (0, 0), image)

    # Save the resulting image
    cropped_image.save(output_path)

    return cropped_image


def section(c, headline, offset, content, color):
    line_space = 23
    c.setFillColor(color)
    c.rect(195, 810 - offset, 390, 25, fill=True, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Calibri-Bold', 14)
    c.drawString(200, 818 - offset, headline)
    c.setFillColor(colors.black)

    for i in range(len(content)):
        if len(content[i]) == 3:
            c.setFont('Calibri-Bold', 14)
            c.drawString(200, 818 - offset - line_space, content[i][0].upper())
            c.setFont('Calibri', 12)
            c.drawString(200, 818 - offset - 13 - line_space, content[i][1])
            c.drawString(200, 818 - offset - 25 - line_space, content[i][2])
            line_space += 50

        elif len(content[i]) == 2:
            c.setFont('Calibri-Bold', 14)
            c.drawString(200, 818 - offset - line_space, content[i][0].upper())
            c.setFont('Calibri', 12)
            c.drawString(200, 818 - offset - 13 - line_space, content[i][1])
            line_space += 35

        elif len(content[i]) == 1:
            c.setFont('Calibri-Bold', 14)
            c.drawString(200, 818 - offset - line_space, content[i][0].upper())
            line_space += 35

    return line_space + 15


def side_section(c, headline, offset, content):
    line_space = 5
    c.setFillColor(colors.white)
    c.setFont('Calibri-Bold', 14)
    c.drawString(10, 843 - offset, headline)

    offset += 10

    c.setFont('Calibri', 8)

    bullet_style = ParagraphStyle(
        'Bullet',
        bulletFontName='Calibri',
        bulletFontSize=8,
        leftIndent=2,
        bulletIndent=2,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    # Calculate the starting y-coordinate for the content
    y = 830 - offset

    # Draw content with bullet points
    for item in content:
        bullet_text = f'<bullet>&bull;</bullet> {item}'
        bullet_paragraph = Paragraph(bullet_text, bullet_style)
        bullet_paragraph.wrapOn(c, 170, 400)  # Adjust width and height as needed
        bullet_height = bullet_paragraph.height
        y -= bullet_height
        bullet_paragraph.drawOn(c, 20, y)
        y -= line_space


class PDFGeneratorEN(DetailView):

    @staticmethod
    def generate_pdf(person):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        #
        one_page_canvas = canvas.Canvas(response, pagesize=A4)
        two_page_canvas = canvas.Canvas(response, pagesize=A4)

        # Retrieve work_experiences
        work_experiences_data = list()
        for exp in person.user.work_experiences.all():
            work_experiences_data.append([f"{exp.last_position}|{exp.company}|{exp.get_status_display()}",
                                          f"{exp.start_date} to {exp.finish_date}|{exp.city}-{exp.country}",
                                          f"{exp.description}"
                                          ])

        # Retrieve educations
        education_data = list()
        for edu in person.user.educations.all():
            education_data.append([f"{edu.degree}|{edu.institute}|{edu.get_status_display()}",
                                   f"{edu.start_date} to {edu.finish_date}|{edu.city}-{edu.country}",
                                   f"{edu.description}"
                                   ])

        # Retrieve skills
        skills_data = list()
        for skill in person.user.skills.all():
            skills_data.append([f"{skill.title}|{skill.level_of_skill}", f"{skill.description}"])

        # Retrieve languages
        languages_data = list()
        for lan in person.user.languages.all():
            languages_data.append([f"{lan.title}|{lan.level_of_language}|{lan.certificate}", f"{lan.description}"])

        # Retrieve projects data
        projects_data = list()
        for pro in person.user.projects.all():
            projects_data.append([f"{pro.title}",
                                  f"{pro.description}"])

        # Retrieve courses data
        courses_data = list()
        for cou in person.user.courses.all():
            courses_data.append([f"{cou.title}|{cou.certificate}|{cou.period}", f"{cou.description}"])

        # Retrieve profile data
        profile_data = list([f"Date of Birth: {person.date_of_birth}",
                             f"Marital Status: {person.get_marital_status_display()}",
                             f"E-MAIL: {person.user.email}",
                             f"PHONE: {person.phone_number}",
                             f"ADDRESS: {person.home_address}"])

        # Retrieve competence data
        competence_data = list()
        for comp in person.user.competences.all():
            competence_data.append(comp)

        # Retrieve hobby data
        hobby_data = list()
        for hob in person.user.hobbies.all():
            hobby_data.append(hob)

        # Retrieve profile and signature images
        user_images = person.user.images.all()

        # Loop through each image object to access profile_image and signature_image
        cropped_profile_image_path = "media/profile_images/default_avatar.jpg"
        signature_image_path = "media/signature_images/default_signature.jpg"

        for image in user_images:
            if image.profile_image:
                profile_image_path = image.profile_image.path
                cropped_profile_image_path = f"{profile_image_path}_cropped.jpg"
                crop_circular(profile_image_path, cropped_profile_image_path, custom_color_EN_cropped)
            if image.signature_image:
                signature_image_path = image.signature_image.path

        # Start of one_page resume design
        one_page_canvas.setFillColor(custom_color_EN)
        one_page_canvas.rect(0, 0, 190, 843, fill=True, stroke=0)
        one_page_canvas.drawImage(cropped_profile_image_path, 20, 675, width=150, height=150)

        one_page_canvas.setFillColor(colors.white)
        one_page_canvas.setFont('Calibri-Bold', 18)
        one_page_canvas.drawString(35, 650, f"{person.first_name_resume} {person.last_name_resume}")
        one_page_canvas.drawString(35, 630, person.user_title)

        side_section(one_page_canvas, 'INFO:', 250, profile_data)
        side_section(one_page_canvas, 'COMPETENCES:', 450, competence_data)
        side_section(one_page_canvas, 'HOBBIES:', 600, hobby_data)

        one_page_canvas.drawImage(signature_image_path, 35, 50, width=120, height=60)

        if work_experiences_data:
            previous_offset = section(one_page_canvas, 'WORK EXPERIENCES', 0,
                                      work_experiences_data, custom_color_EN)
        else:
            previous_offset = 0

        if education_data:
            offset = section(one_page_canvas, 'EDUCATIONS', previous_offset, education_data, custom_color_EN)
            new_offset = offset + previous_offset
        else:
            new_offset = previous_offset

        if skills_data:
            offset = section(one_page_canvas, 'SKILLS', new_offset, skills_data, custom_color_EN)
            new_offset = offset + new_offset

        if languages_data:
            offset = section(one_page_canvas, 'LANGUAGES', new_offset, languages_data, custom_color_EN)
            new_offset = offset + new_offset

        if projects_data:
            offset = section(one_page_canvas, 'PROJECTS', new_offset, projects_data, custom_color_EN)
            new_offset = offset + new_offset

        if courses_data:
            offset = section(one_page_canvas, 'COURSES', new_offset, courses_data, custom_color_EN)
            new_offset = offset + new_offset

        if new_offset < 810:

            print("new offset of one page is:", new_offset)
            print('Offset is smaller than 800, then we do it in one page')

            one_page_canvas.showPage()
            one_page_canvas.save()
            return response
        else:
            print("new offset of one page is:", new_offset)
            print('Offset is bigger than 800, then we do it in one page')

            # Start of two_page resume design
            two_page_canvas.setFillColor(custom_color_EN)
            two_page_canvas.rect(0, 0, 190, 843, fill=True, stroke=0)
            two_page_canvas.drawImage(cropped_profile_image_path, 20, 675, width=150, height=150)

            two_page_canvas.setFillColor(colors.white)
            two_page_canvas.setFont('Calibri-Bold', 18)
            two_page_canvas.drawString(35, 650, f"{person.first_name_resume} {person.last_name_resume}")
            two_page_canvas.drawString(35, 630, person.user_title)

            side_section(two_page_canvas, 'INFO:', 250, profile_data)
            side_section(two_page_canvas, 'COMPETENCES:', 450, competence_data)
            side_section(two_page_canvas, 'HOBBIES:', 600, hobby_data)

            two_page_canvas.drawImage(signature_image_path, 35, 50, width=120, height=60)

            if work_experiences_data:
                previous_offset = section(two_page_canvas, 'WORK EXPERIENCES', 0,
                                          work_experiences_data, custom_color_EN)
            else:
                previous_offset = 0

            if education_data:
                offset = section(two_page_canvas, 'EDUCATIONS', previous_offset,
                                 education_data, custom_color_EN)
                new_offset = offset + previous_offset
            else:
                new_offset = previous_offset

            if languages_data:
                offset = section(two_page_canvas, 'LANGUAGES', new_offset, languages_data, custom_color_EN)
                new_offset = offset + new_offset

            two_page_canvas.showPage()
            two_page_canvas.setFillColor(custom_color_EN)
            two_page_canvas.rect(0, 0, 190, 843, fill=True, stroke=0)

            if skills_data:
                offset = section(two_page_canvas, 'SKILLS', 0, skills_data, custom_color_EN)
                new_offset = offset

            if projects_data:
                offset = section(two_page_canvas, 'PROJECTS', new_offset, projects_data, custom_color_EN)
                new_offset = offset + new_offset

            if courses_data:
                offset = section(two_page_canvas, 'COURSES', new_offset, courses_data, custom_color_EN)
                new_offset = offset + new_offset

            print(new_offset)
            two_page_canvas.showPage()
            two_page_canvas.save()
            return response


class PDFGeneratorDE(DetailView):

    @staticmethod
    def generate_pdf(person):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resumeDE.pdf"'
        #
        one_page_canvas = canvas.Canvas(response, pagesize=A4)
        two_page_canvas = canvas.Canvas(response, pagesize=A4)

        # Retrieve work_experiences
        work_experiences_data = list()
        for exp in person.user.arbeit_erfahrung.all():
            work_experiences_data.append([f"{exp.last_position}| {exp.company}|{exp.get_status_display()}",
                                          f"{exp.start_date}-{exp.finish_date}|{exp.city}-{exp.country}",
                                          f"{exp.description}"
                                          ])

        # Retrieve educations
        education_data = list()
        for edu in person.user.ausbildung.all():
            education_data.append([f"{edu.degree}| {edu.institute}|{edu.get_status_display()}|{edu.average}",
                                   f"{edu.start_date}-{edu.finish_date}|{edu.city}-{edu.country}",
                                   f"{edu.description}"
                                   ])

        # Retrieve skills
        skills_data = list()
        for skill in person.user.fahigkeiten.all():
            skills_data.append([f"{skill.title}|{skill.level_of_skill}", f"{skill.description}"])

        # Retrieve languages
        languages_data = list()
        for lan in person.user.sprachen.all():
            languages_data.append([f"{lan.title}|{lan.level_of_language}|{lan.certificate}", f"{lan.description}"])

        # Retrieve projects data
        projects_data = list()
        for pro in person.user.projekte.all():
            projects_data.append([f"{pro.title}|{pro.description}"])

        # Retrieve courses data
        courses_data = list()
        for cou in person.user.kurse.all():
            courses_data.append([f"{cou.title}|{cou.certificate}|{cou.period}", f"{cou.description}"])

        # Retrieve profile data
        profile_data = list([f"Geburtsdatum: {person.date_of_birth}",
                             f"Familiarities: {person.get_marital_status_display()}",
                             f"E-MAIL: {person.user.email}",
                             f"HANDY: {person.phone_number}",
                             f"ADDRESS: {person.home_address}"])

        # Retrieve competence data
        competence_data = list()
        for comp in person.user.kompetenzen.all():
            competence_data.append(comp)

        # Retrieve hobby data
        hobby_data = list()
        for hob in person.user.hobbys.all():
            hobby_data.append(hob)

        # Retrieve profile and signature images
        user_images = person.user.fotos.all()

        # Loop through each image object to access profile_image and signature_image
        cropped_profile_image_path = "media/profile_images/default_avatar.jpg"
        signature_image_path = "media/signature_images/default_signature.jpg"

        for image in user_images:
            if image.profile_image:
                profile_image_path = image.profile_image.path
                cropped_profile_image_path = f"{profile_image_path}_cropped_DE.jpg"
                crop_circular(profile_image_path, cropped_profile_image_path, custom_color_DE_cropped)
            if image.signature_image:
                signature_image_path = image.signature_image.path

        # Start of one_page resume design
        one_page_canvas.setFillColor(custom_color_DE)
        one_page_canvas.rect(0, 0, 190, 843, fill=True, stroke=0)
        one_page_canvas.drawImage(cropped_profile_image_path, 20, 675, width=150, height=150)

        one_page_canvas.setFillColor(colors.white)
        one_page_canvas.setFont('Calibri-Bold', 18)
        one_page_canvas.drawString(35, 650, f"{person.first_name_resume} {person.last_name_resume}")
        one_page_canvas.drawString(35, 630, person.user_title)

        side_section(one_page_canvas, 'INFO:', 250, profile_data)
        side_section(one_page_canvas, 'KOMPETENZEN:', 450, competence_data)
        side_section(one_page_canvas, 'HOBBYS:', 600, hobby_data)

        one_page_canvas.drawImage(signature_image_path, 35, 50, width=120, height=60)

        if work_experiences_data:
            previous_offset = section(one_page_canvas, 'ARBEITSERFAHRUNG', 0,
                                      work_experiences_data, custom_color_DE)
        else:
            previous_offset = 0

        if education_data:
            offset = section(one_page_canvas, 'AUSBILDUNG', previous_offset, education_data, custom_color_DE)
            new_offset = offset + previous_offset
        else:
            new_offset = previous_offset

        if skills_data:
            offset = section(one_page_canvas, 'FÄHIGKEITEN', new_offset, skills_data, custom_color_DE)
            new_offset = offset + new_offset

        if languages_data:
            offset = section(one_page_canvas, 'SPRACHEN', new_offset, languages_data, custom_color_DE)
            new_offset = offset + new_offset

        if projects_data:
            offset = section(one_page_canvas, 'PROJEKTE', new_offset, projects_data, custom_color_DE)
            new_offset = offset + new_offset

        if courses_data:
            offset = section(one_page_canvas, 'KURSE', new_offset, courses_data, custom_color_DE)
            new_offset = offset + new_offset

        if new_offset < 810:

            print("new offset of one page is:", new_offset)
            print('Offset is smaller than 800, then we do it in one page')

            one_page_canvas.showPage()
            one_page_canvas.save()
            return response
        else:
            print("new offset of one page is:", new_offset)
            print('Offset is bigger than 800, then we do it in one page')

            # Start of two_page resume design
            two_page_canvas.setFillColor(custom_color_DE)
            two_page_canvas.rect(0, 0, 190, 843, fill=True, stroke=0)
            two_page_canvas.drawImage(cropped_profile_image_path, 20, 675, width=150, height=150)

            two_page_canvas.setFillColor(colors.white)
            two_page_canvas.setFont('Calibri-Bold', 18)
            two_page_canvas.drawString(35, 650, f"{person.first_name_resume} {person.last_name_resume}")
            two_page_canvas.drawString(35, 630, person.user_title)

            side_section(two_page_canvas, 'INFO:', 250, profile_data)
            side_section(two_page_canvas, 'KOMPETENZEN:', 450, competence_data)
            side_section(two_page_canvas, 'HOBBYS:', 600, hobby_data)

            two_page_canvas.drawImage(signature_image_path, 35, 50, width=120, height=60)

            if work_experiences_data:
                previous_offset = section(two_page_canvas, 'ARBEITSERFAHRUNG', 0,
                                          work_experiences_data, custom_color_DE)
            else:
                previous_offset = 0

            if education_data:
                offset = section(two_page_canvas, 'AUSBILDUNG', previous_offset,
                                 education_data, custom_color_DE)
                new_offset = offset + previous_offset
            else:
                new_offset = previous_offset

            if languages_data:
                offset = section(two_page_canvas, 'SPRACHEN', new_offset, languages_data, custom_color_DE)
                new_offset = offset + new_offset

            two_page_canvas.showPage()
            two_page_canvas.setFillColor(custom_color_DE)
            two_page_canvas.rect(0, 0, 190, 843, fill=True, stroke=0)

            if skills_data:
                offset = section(two_page_canvas, 'FÄHIGKEITEN', 0, skills_data, custom_color_DE)
                new_offset = offset

            if projects_data:
                offset = section(two_page_canvas, 'PROJEKTE', new_offset, projects_data, custom_color_DE)
                new_offset = offset + new_offset

            if courses_data:
                offset = section(two_page_canvas, 'KURSE', new_offset, courses_data, custom_color_DE)
                new_offset = offset + new_offset

            print(new_offset)
            two_page_canvas.showPage()
            two_page_canvas.save()
            return response

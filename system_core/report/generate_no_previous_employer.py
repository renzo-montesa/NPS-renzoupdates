from api.v1.employee_info.model import EmployeeInfoModel
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER
import config
import datetime
import sys


REPORT_PATH = config.REPORT_DIR


def generate_no_previous_employer(data):
    print("Start | Generate no previous employer data report", file=sys.stderr)

    data = {}

    data['report'] = {
        'title': 'No Previous Employer Data Report'
    }
    data['options'] = {
        'date_range': {
            'from': '01/01/2020',
            'to': '12/31/2020'
        }
    }
    data['company'] = {
        'name': 'Test Company'
    }
    data['employees'] = EmployeeInfoModel.get_no_prev_employer_data()
    now = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    canvas = Canvas(REPORT_PATH + "test.pdf", pagesize=LETTER)

    """ Initialize pdf values """
    page = 1

    count = len(data['employees'])
    ctr = 0

    while ctr < count:
        add_header(canvas, data, now, page)
        ctr = add_body(canvas, data, ctr)
        page += 1
        canvas.showPage()

    """ Save pdf file """
    canvas.save()

    print("Finished | Generate no previous employer data report", file=sys.stderr)


def add_header(canvas, data, now, page):
    """ Draw page header start """
    canvas.setFont("Courier", 8)
    canvas.drawString(36, 720, "Run Date/Time " + now)
    canvas.drawRightString(576, 720, "Page " + str(page))

    canvas.setFont("Courier", 10)
    canvas.drawCentredString(306, 684, data['company']['name'])

    canvas.setFont("Courier", 12)
    canvas.drawCentredString(306, 670, data['report']['title'])

    canvas.setFont("Courier", 10)
    canvas.drawCentredString(306, 656, data['options']['date_range']['from'] + " - " + data['options']['date_range']['to'])

    canvas.setLineWidth(0.5)
    canvas.line(72, 636, 540, 636)

    canvas.setFont("Courier", 9)
    canvas.drawString(86, 624, "Employee No")
    canvas.drawString(160, 624, "Name")
    canvas.drawString(432, 624, "Hiring Date")

    canvas.line(72, 618, 540, 618)
    """ Draw page header end """

def add_body(canvas, data, ctr):
    """ Draw page body start """
    """ Initialize values """
    row = 608
    count = len(data['employees'])
    canvas.setFont("Courier", 8)

    while row > 72 and ctr < count:
        name = data['employees'][ctr]['lastname'] + ", " + data['employees'][ctr]['firstname']
        if data['employees'][ctr]['middlename']:
            name += " " + data['employees'][ctr]['middlename'][0] + "."

        canvas.drawString(86, row, data['employees'][ctr]['employee_number'])
        canvas.drawString(160, row, name)
        canvas.drawString(432, row, convert_date(data['employees'][ctr]['hired_date']))

        row -= 10
        ctr += 1
    """ Draw page body end """

    return ctr


def convert_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")
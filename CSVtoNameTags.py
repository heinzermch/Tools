# Take input from a CSV and create name tags with flags and occupation
# Store output as PDF
import pycountry
import labels
import os.path
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from reportlab.graphics import shapes
from PIL import Image


class Person:
    status = ""
    name = ""
    country_name = ""
    country_code = ""
    university = ""

    def __init__(self, status, name, country_name, country_code, university):
        self.status = status
        self.name = name
        self.country_name = country_name
        self.country_code = country_code
        self.university = university
        self.complete()

    def complete(self):
        if self.university == "":
            self.university = "None"
        if self.country_code == "":
            country = pycountry.countries.get(name=self.country_name)
            self.country_code =  country.alpha_2.encode('ascii')
        if self.country_name == "":
            country = pycountry.countries.get(alpha_2=self.country_code)
            if self.country_code == "BO":
                self.country_name = "Bolivia"
            elif self.country_code == "PS":
                self.country_name = "Palestine"
            elif self.country_code == "MK":
                self.country_name = "Macedonia"
            elif self.country_code == "IR":
                self.country_name = "Iran"
            elif self.country_code == "KR":
                self.country_name = "South Korea"
            else:
                self.country_name = country.name.encode('ascii')

    def to_string(self):
        return self.name + " is " + self.status + " from " + self.university + " going to " + self.country_code + "/" + self.country_name

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 9 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(210, 297, 3, 9, 60, 20, corner_radius=2)
specs.top_margin = 20
specs.bottom_margin = 20


# Get the path to the demos directory.
base_path = os.path.dirname(__file__)

# Add some fonts.
registerFont(TTFont('Judson Bold', base_path + '/fonts/' + 'JudsonBold.ttf'))
registerFont(TTFont('KatamotzIkasi', os.path.join(base_path, 'fonts', 'KatamotzIkasi.ttf')))

def write_name(label, width, height, person):
    name = person.name
    status = person.status
    university = person.university
    country = person.country_name
    code = person.country_code
    # Write the title.
    text_width = width - 10
    font_size = 15
    name_width = stringWidth(name, "Judson Bold", font_size)
    while name_width > text_width:
        font_size *= 0.9
        name_width = stringWidth(name, "Judson Bold", font_size)
    label.add(shapes.String(5, height-font_size, name,
                            fontName="Judson Bold", fontSize=font_size))
    if status == "Outgoer":
        label.add(shapes.String(5, height - 30, status + " " +university,
                            fontName="Judson Bold", fontSize=12))
    else:
        label.add(shapes.String(5, height - 30, person.status,
                                fontName="Judson Bold", fontSize=12))
    label.add(shapes.String(5, height - 45, country,
                                fontName="Judson Bold", fontSize=10))

    imgpath = "flags/"+code+".png"
    ratio = 0
    try:
        im = Image.open(imgpath)
        width, height = im.size
        ratio = (0.0 + width) / height
        x = 120
        y = 5
        if width > height:
            width = 40
            height = 1/ratio * width
        else:
            height = 40
            width = ratio * height
        label.add(shapes.Image(x, y, width, height, imgpath))
    except IOError:
        print("No flag for " + imgpath + " or country " + country)

    if status == "LC Member" or status == "National Office":
        label.add(shapes.Image(80, 10, 35, 15, "iaeste.png"))

people = []
my_file = open("completedata.csv", "rb")
first = True
print("Reading data from csv")
for line in my_file:
    if first:
        first = False
        continue
    l = [i.strip() for i in line.split(',')]
    people += [Person(l[0],l[1],l[2],l[3],l[4])]

for person in people:
    print person.to_string()

print("Creating labels")
# Create the sheet.
sheet = labels.Sheet(specs, write_name, border=False)

# Create the name tags from the people objects
sheet.add_labels(people)

# Print the pdf
sheet.save('nametags.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
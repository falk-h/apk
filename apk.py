import xml.etree.ElementTree as ET
import sys
import datetime
import math

# Returns alcohol per krona for a drink, in ml/kr
# Includes the deposit for cans in the calculated price
def apk(drink):
    price = float(drink.find('Prisinklmoms').text)
    abv = float(drink.find('Alkoholhalt').text.strip('%'))/100 # Alcohol by volume (0-1)
    size = float(drink.find('Volymiml').text)

    if drink.find('Forpackning').text == 'Burk':
        price += 1.0 # Add deposit
    return abv * size / price

# Returns alcohol per krona for a drink if it were sold in Basen, in ml/kr
# Includes the deposit for cans in the calculated price
def basenApk(drink):
    price = basenPrice(drink)
    abv = float(drink.find('Alkoholhalt').text.strip('%'))/100 # Alcohol by volume (0-1)
    size = float(drink.find('Volymiml').text)

    return abv * size / price

# Returns the price a drink would have if it was sold in Basen
# The price is calculated as the price from Systembolaget (including deposit) 
# plus 25%, rounded up to the next five kronor. In addition to this, 33cl drinks
# may not cost less than 20 kr, and 500 ml drinks may not cost less than 30 kr.
def basenPrice(drink):
    price = float(drink.find('Prisinklmoms').text)
    size = float(drink.find('Volymiml').text)

    if drink.find('Forpackning').text == 'Burk':
        price += 1.0 # Add deposit

    price = math.ceil(price*1.25/5)*5

    if size < 400:
        return max(price, 20)
    else:
        return max(price, 30)

# Returns False for non-alcoholic products, like gift boxes and water
def hasAlcohol(drink):
    abv = float(drink.find('Alkoholhalt').text.strip('%')) # Alcohol by volume
    return abv > 0.0

# Returns true for products in the specified range
# The ranges seem to be
# BS   Beställningssortiment
# FSB  Ordinarie sortiment
# FSN  Ordinarie sortiment
# FSÖ  Alkoholfritt
# FS   Ordinarie sortiment
# TSE  Små partier
# TSLS Lokalt och småskaligt
# TSS  Säsongsdrycker
# TST  No idea
# TSV  No idea
# No idea what TST and TSV are. They also only have three entries between them.
# Also not sure on the difference between FSB, FSN, and FS
def inRange(drink, range):
    return drink.find('Sortiment').text == range

# Possible types are
# Akvavit och Kryddat brännvin, Alkoholfritt, Anissprit, Aperitif och dessert
# Armagnac och Brandy, Bitter, Blå mousserande, Blanddrycker, Blå stilla, Calvados
# Cider, Cognac, Drinkar och Cocktails, Frukt och Druvsprit, Gin och Genever
# Glögg och Glühwein, Grappa och Marc, Likör, Mousserande vin, Öl, Punsch, Röda
# Rom, Rosé, Rosévin, Rött vin, Sake, Smaksatt sprit, Sprit av flera typer
# Tequila och Mezcal, Vermouth, Vita, Vitt vin, Vodka och Brännvin, Whisky

if (len(sys.argv) != 2):
    print("Usage: python {} <infile>".format(sys.argv[0]))
    sys.exit(1)


inFile = sys.argv[1]

tree = ET.parse(inFile)
root = tree.getroot()
articles = root.findall("artikel")

# Filter out articles with zero alcohol, in the store pickup range, in the
# locally produced range, and articles that are no longer carried
drinks = [article for article in articles if hasAlcohol(article) 
                                             and not inRange(article, 'BS')
                                             and not inRange(article, 'TSLS')
                                             and article.find('Utgått').text == '0']

wineTypes = ['Aperitif och dessert', 'Blå mousserande', 'Blå stilla',
             'Glögg och Glühwein', 'Mousserande vin', 'Röda', 'Rosé', 'Rosévin',
             'Rött vin', 'Vermouth', 'Vita', 'Vitt vin']

liquorTypes = ['Akvavit och Kryddat brännvin', 'Anissprit',
               'Armagnac och Brandy', 'Bitter', 'Calvados', 'Cognac',
               'Frukt och Druvsprit', 'Gin och Genever', 'Grappa och Marc',
               'Likör', 'Punsch', 'Rom', 'Smaksatt sprit',
               'Sprit av flera typer', 'Tequila och Mezcal',
               'Vodka och Brännvin', 'Whisky']

otherTypes = ['Blanddrycker', 'Drinkar och Cocktails', 'Sake']

beers = [drink for drink in drinks if drink.find('Varugrupp').text == 'Öl']
ciders = [drink for drink in drinks if drink.find('Varugrupp').text == 'Cider']
wines = [drink for drink in drinks if drink.find('Varugrupp').text in wineTypes]
liquors = [drink for drink in drinks if drink.find('Varugrupp').text in liquorTypes]
others = [drink for drink in drinks if drink.find('Varugrupp').text in otherTypes]

categories = [['Öl', beers], ['Cider', ciders], ['Vin', wines],
              ['Sprit', liquors], ['Resten', others]]

print('<!-- Generated at {} -->\nKategorier:'.format(datetime.datetime.now()))

for category in categories:
    print('&nbsp;<a href="#{}">{}</a>'.format(category[0], category[0]))
    category[1].sort(key=apk, reverse=True)

basenBeers = beers.copy()
basenCiders = ciders.copy()

basenCategories = [['Basenöl', basenBeers], ['Basencider', basenCiders]]

for category in basenCategories:
    print('&nbsp;<a href="#{}">{}</a>'.format(category[0], category[0]))
    category[1].sort(key=basenApk, reverse=True)
    categories.append(category)

print('<br/><br/>')

for category in categories:
    print('<br id="{}"/><h2>{}!</h2><table><tr><th/><th>APK</th><th>Namn</th><th>Stil</th><th>Förpackning</th><th>Alkoholhalt</th><th>Storlek</th><th>Pris (ink pant)</th></tr>'.format(category[0], category[0]))
    for index, drink in enumerate(category[1]):
        drinkApk=''
        price=''
        if category[0].startswith('Basen'):
            drinkApk='{0:.5g}&nbsp;ml/kr'.format(basenApk(drink))
            price = '{0:.2f}&nbsp;kr'.format(basenPrice(drink))
        else:
            drinkApk='{0:.5g}&nbsp;ml/kr'.format(apk(drink))
            price = '{0:.2f}&nbsp;kr'.format(float(drink.find('Prisinklmoms').text) + (1 if drink.find('Forpackning').text == 'Burk' else 0))
        name = ''
        if drink.find('Namn2').text == None:
            name = drink.find('Namn').text
        else:
            name = '{} {}'.format(drink.find('Namn').text, drink.find('Namn2').text)
        style = drink.find('Stil').text if drink.find('Stil').text != None else drink.find('Varugrupp').text
        packaging = drink.find('Forpackning').text
        abv = drink.find('Alkoholhalt').text
        size = '{0:.5g}&nbsp;ml'.format(float(drink.find('Volymiml').text))
        number = drink.find('nr').text

        print('<tr><td class="id">{}</td><td>{}</td><td><a href="https://systembolaget.se/{}">{}</a></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
                .format(index, drinkApk, number, name, style, packaging, abv, size, price))
    print('</table>')

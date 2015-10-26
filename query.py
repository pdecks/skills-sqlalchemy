"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()

# -------------------------------------------------------------------
# Start here.


# Part 2: Write queries

# Get the brand with the **id** of 8.
Brand.query.filter_by(id=8).one()

# Get all models with the **name** Corvette and the **brand_name** Chevrolet.
Model.query.filter_by(name="Corvette", brand_name="Chevrolet").all()

# Get all models that are older than 1960.
Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor".
Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands with that were founded in 1903 and that are not yet discontinued.
Brand.query.filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either discontinued or founded before 1950.
Brand.query.filter((Brand.discontinued != None) | (Brand.founded < 1950)).all()

# Get any model whose brand_name is not Chevrolet.
Model.query.filter(Model.brand_name != "Chevrolet").all()

# Fill in the following functions. (See directions for more info.)


def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.

    >>> get_model_info(1953)
    <BLANKLINE>
    MODELS IN YEAR 1953
    ------------------------------
    Model: Corvette
    Make: Chevrolet
    Headquarters: Detroit, Michigan
    ------------------------------
    '''

    models_and_brands = db.session.query(Model.name, Model.brand_name, Brand.headquarters).join(Brand, Brand.name==Model.brand_name).filter(Model.year == year).all()

    # QUERY = """
    # SELECT Models.name, Models.brand_name, Brands.headquarters
    # FROM Models
    # JOIN Brands ON Models.brand_name = Brands.name
    # WHERE Models.year = :year;
    # """

    # cursor = db.session.execute(QUERY, {'year': year})
    # models_and_brands = cursor.fetchall()
    
    print "\nMODELS IN YEAR %s" % year
    print "-"*30
    for pair in models_and_brands:
        model_name, model_make, brand_hq = pair
        print "Model: %s" % model_name
        print "Make: %s" % model_make
        print "Headquarters: %s" % brand_hq
        print "-"*30
    return


def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
    using only ONE database query.

    '''
    # models_by_brand = db.session.query(Model.brand_name, Model.name).group_by(Model.brand_name).all()
    
    models_by_brand = Model.query.order_by(Model.brand_name).all()
    brand = ''

    print "\nBRANDS SUMMARY"
    for model in models_by_brand:
        if model.brand_name != brand:
            brand = model.brand_name
            print '-'*30
            print "%s" % brand.upper()
        print "%s | %s" % (model.name, model.year)
    return

# -------------------------------------------------------------------


# Part 2.5: Advanced and Optional
def search_brands_by_name(mystr):
    """Takes in any string as parameter and returns a list of objects
    that are brands whose name contains or is equal to the input string.

    >>> my_list = search_brands_by_name('ord')
    >>> my_list[0].name
    u'Ford'

    """
    search_str = "%"+mystr+"%"
    brands_list = Brand.query.filter(Brand.name.like(search_str)).all()
    return brands_list


def get_models_between(start_year, end_year):
    """Takes a start year and end year (two integers) and returns a list of objects
    that are models with years that fall between those years.

    >>> my_list = get_models_between(1963,1965)
    >>> my_list[0].name
    u'Corvette'

    """
    models_list = Model.query.filter((Model.year > start_year) & (Model.year < end_year)).all()
    return models_list


# -------------------------------------------------------------------

# Part 3: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?
# The returned datatype is an object, specifically a BaseQuery, because we did not 
# fetch the records from the object by using .all(), .one(), etc. 

# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?
# An association table describes a many-to-many relationship, storing information about how entries
# from one table are related to entries in another table. For example, in our ratings exercise,
# the ratings table desribes the relationship between users and movies. In our lecture notes, the
# bookgenre table is association table that describes the many-to-many relationship between
# books and genres. An association table may or may not have information independent of the tables
# it connects.

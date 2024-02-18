from ScrapData import ScrapData
from GenerateDF import GenerateDF
from CreateVectorDB import CreateVectorDB
from ResponseGenerator import ResponseGenerator
import warnings

warnings.filterwarnings("ignore",category=UserWarning)
warnings.filterwarnings("ignore")

def GenerateResponse(prompt="cars"):
    # get the user prompt
    # prompt=input("Please enter prompt...\n")
    # if prompt=="":
    #     prompt="cars"
        
    # scraped data csv filename
    csv_filename='data.csv'

    # scraping data using obj
    SD = ScrapData(prompt=prompt,num_results=100)
    results = SD.scrap()

    # generating DF of scraped data using obj
    GDF=GenerateDF(results=results)
    GDF.generate_df()

    # saving the scraped data in csv file
    GDF.save(filename=csv_filename)

    # creating vector db using sqlite3
    db=CreateVectorDB(csv_filename)
    db.createDb()

    # enhance the prompt and generate the summary
    RG=ResponseGenerator(prompt=prompt)

    return RG.generate_summary()


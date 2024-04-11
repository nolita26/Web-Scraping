from bs4 import BeautifulSoup
import csv
import requests

def getData(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    #soup.find("div",class_="toc") #class cannot be used as parameter directly in Python, therefore, use class_
    #soup.find("div",{"class": "toc", "id":"toc"}) #By using a dictionary, more than one attribute can be specified
    table_of_contents = soup.find("div", id="toc")

    #find_all method will return a list of elements, so we can iterate over it
    headings = table_of_contents.find_all("li")

    data = []
    for heading in headings:
        heading_text = heading.find("span", class_="toctext").text #To get the text inside the element, use the text attribute
        heading_number = heading.find("span", class_="tocnumber").text #Heading numbers are extracted
        data.append({
            'heading_number': heading_number,
            'heading_text': heading_text,
        })
    return data

def saveData(data, file_name):
    with open(file_name, "w", newline="") as file: #Explore the data

        #Create an instance of DictWriter object. This needs a list of headers. In this case, it's going to be the dictionary keys in the data.
        writer = csv.DictWriter(file, fieldnames=['heading_number', 'heading_text'])
        writer.writeheader()
        writer.writerows(data) #Method to write the data

def main():
    url_to_parse = "https://nextjs.org/docs"
    file_name = "result1.csv"
    data = getData(url_to_parse)
    saveData(data, file_name)
    print('Data saved!')

if __name__ == '__main__':
    main()
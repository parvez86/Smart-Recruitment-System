import glob
import os
import warnings
import textract
import requests, re
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.neighbors import NearestNeighbors
import PyPDF2
from json import load, dumps
from operator import getitem
from collections import OrderedDict
from .text_process import normalize
from nltk.tokenize import word_tokenize

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


def getFilePath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def getFileName(filename):
    return filename.rsplit('\\')[1]


def readResultInJson(jobfile='job1'):
    filepath = 'result/'
    with open(filepath + jobfile + '.json', 'r') as openfile:
        # Reading from json file
        result = load(openfile)
    return result


def writeResultInJson(data, jobfile='job1'):
    filepath = 'result/'
    json_str = dumps(data, indent=4)
    with open(filepath + jobfile + '.json', 'w+', encoding='utf-8') as f:
        f.write(json_str)
        f.close()


def get_rank(result_dict=None):

    if result_dict == None:
        return {}

    # new_result_dict = sorted(result_dict.items(), key=lambda item: float(item[1]["score"]), reverse=False)
    new_result_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: getitem(item[1], 'score'), reverse=False))
    new_updated_result_dict = {}
    indx = 0
    for _, item in new_result_dict.items():
        item['rank'] = indx + 1
        new_updated_result_dict[indx] = item
        indx += 1
    return new_updated_result_dict


def show_rank(result_dict=None, jobfileName='job1', top_k=20):
    if (result_dict == None):
        filepath = 'result/' + jobfileName + '.json'
        result_dict = readResultInJson(filepath)
    print("\nResult:")
    for _, result in result_dict.items():
        # print(result)
        print(f"Rank: {result['rank']}\t Total Score:{round(result['score'], 5)} (NN distance) \tName:{result['name']}")
# start parse


def res(job_desc, list_of_resumes, jobfilename):
    Resume_Vector = []
    Ordered_list_Resume = []
    Resumes = []
    Temp_pdf = []

    # resumes file path
    filepath = 'media/'

    # for file in glob.glob(filepath + '**/*.pdf', recursive=True):
    #     LIST_OF_FILES_PDF.append(file)
    #     print(file)
    # for file in glob.glob(filepath + '**/*.doc', recursive=True):
    #     LIST_OF_FILES_DOC.append(file)
    # for file in glob.glob(filepath + '**/*.docx', recursive=True):
    #     LIST_OF_FILES_DOCX.append(file)
    # LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF

    LIST_OF_FILES = list_of_resumes

    print("Total Files to Parse\t", len(LIST_OF_FILES))
    print("####### PARSING ########")
    for indx, file in enumerate(LIST_OF_FILES):
        Ordered_list_Resume.append(file)
        Temp = file.split('.')

        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                # print("This is PDF", indx)
                with open(filepath + file, 'rb') as pdf_file:
                    read_pdf = PyPDF2.PdfFileReader(pdf_file)

                    number_of_pages = read_pdf.getNumPages()
                    for page_number in range(number_of_pages):
                        page = read_pdf.getPage(page_number)
                        page_content = page.extractText()
                        page_content = page_content.replace('\n', ' ').replace('\f', '').replace('\\uf[0-9]+',
                                                                                                 '').replace(
                            '\\u[0-9]+', '').replace('\\ufb[0-9]+', '')
                        # page_content.replace("\r", "")

                        Temp_pdf = str(Temp_pdf) + str(page_content)
                        # print(Temp_pdf)

                    Resumes.extend([Temp_pdf])
                    Temp_pdf = ''

                    # f = open(str(i)+str("+") , 'w')
                    # f.write(page_content)
                    # f.close()
            except Exception as e:
                print(e)

        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
            # print("This is DOC", file)

            try:
                a = textract.process(filepath)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
            except Exception as e:
                print(e)

        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            # print("This is DOCX", file)
            try:
                a = textract.process(filepath+file)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
            except Exception as e:
                print(e)

        if Temp[1] == "exe" or Temp[1] == "Exe" or Temp[1] == "EXE":
            # print("This is EXE", file)
            pass
    print("Done Parsing.")

    Job_Desc = 0
    LIST_OF_TXT_FILES = []
    job_desc_filepath = 'jobDetails/'

    # with open(job_desc_filepath + jobfile, 'r') as f:
    #     text = re.sub(' +', ' ', f.read())
    #     f.close()
    print('Sample job description: \n', job_desc)
    try:
        text = re.sub(' +', ' ', job_desc)
        tttt = str(text)
        tttt = normalize(word_tokenize(tttt))
        text = [' '.join(tttt)]
    except:
        text = 'None'
    print("\nNormalized Job Description:\n", text)


    # get tf-idf
    vectorizer = CountVectorizer(stop_words='english')
    transformar = TfidfTransformer()
    vectorizer.fit(text)
    vector = transformar.fit_transform(vectorizer.transform(text).toarray())
    Job_Desc = vector.toarray()
    print("\nTF-IDF weight  (For Job Description):\n", Job_Desc, '\n')


    for file in Resumes:
        text = file
        tttt = str(text)
        try:

            tttt = normalize(word_tokenize(tttt))
            text = [' '.join(tttt)]

            vector = transformar.fit_transform(vectorizer.transform(text).toarray())

            aaa = vector.toarray()
            print("TF-IDF weight(For Resumes): \n", aaa)
            Resume_Vector.append(aaa)
        except:
            pass

    # ranking process
    result_arr = dict()
    for indx, file in enumerate(Resume_Vector):
        samples = file
        name = Ordered_list_Resume[indx]
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples)
        NearestNeighbors(algorithm='auto', leaf_size=30)

        # score = round(neigh.kneighbors(Job_Desc)[0][0][0], 5)
        score = neigh.kneighbors(Job_Desc)[0][0][0]
        # print(score)
        result_arr[indx] = {'name': name, 'score': score}

    result_arr = get_rank(result_arr)
    writeResultInJson(result_arr, jobfilename)
    show_rank(result_arr, jobfilename)

    return result_arr


# if __name__ == '__main__':
#     inputStr = input("")
#     # sear(inputStr)

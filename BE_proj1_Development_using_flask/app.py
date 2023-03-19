# Step 1 - To import FLASK
from flask import Flask, request, render_template
import re

# Step 2 - Create the object with a parameter __name__
app = Flask(__name__)


###################################################
# Step 3 - Create an END POINT using routes and bind them with a functionality


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        return "Welcome to the search page using POST Req"
    else:
        return render_template('search.html')

@app.route('/search_pattern_regex', methods=['POST','GET'])
def search_pattern_regex():
    if request.method=="POST":
        output_list=[]
        regex=request.form.get('regex')
        text_string=request.form.get('string')
        for index,element in enumerate(re.findall(regex,text_string)):
            span=re.search(element,text_string).span()
            output_list.append(f'Start: {span[0]} End: {span[1]} Substring {element}')
        return render_template('output.html',len=len(output_list),output_list=output_list)
    else:
        return render_template('search.html')




###################################################

# Step 4 - Run the app
if __name__ == '__main__':
    app.run(debug=True,port=8000)
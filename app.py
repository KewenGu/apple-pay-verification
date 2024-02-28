from flask import Flask, send_file, request, render_template_string
import os

app = Flask(__name__)

# Configure upload folder and max upload size (e.g., 16MB)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def home():
    return render_template_string("""
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/carbon-components@10/css/carbon-components.min.css">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            .wrapper {
                padding: 2rem 3%;
            }
            .bx--form-item {
                margin-bottom: 1.5rem;
            }
            .bx--select__arrow {
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="wrapper bx--grid" style="background: white;">
            <form action="/submit" method="post" enctype="multipart/form-data">
                <div class="bx--form-item">
                    <label for="product-name" class="bx--label">Product Name</label>
                    <input id="product-name" name="product-name" type="text" class="bx--text-input">
                </div>
                <div class="bx--form-item">
                    <div class="bx--row">
                        <div class="bx--col-lg-8 bx--col-md-4 bx--col-sm-2">
                            <label for="product-weight" class="bx--label">Product Weight</label>
                            <input id="product-weight" name="product-weight" type="number" class="bx--text-input">
                        </div>
                        <div class="bx--col-lg-8 bx--col-md-4 bx--col-sm-2">
                            <div class="bx--select">
                                <label for="select-weight-unit" class="bx--label">Unit</label>
                                <select id="select-weight-unit" class="bx--select-input">
                                    <option class="bx--select-option" value="oz">oz</option>
                                    <option class="bx--select-option" value="lb">lb</option>
                                    <option class="bx--select-option" value="lb">g</option>
                                    <option class="bx--select-option" value="lb">kg</option>
                                </select>
                                <svg focusable="false" preserveAspectRatio="xMidYMid meet" style="will-change: transform;" xmlns="http://www.w3.org/2000/svg" class="bx--select__arrow" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 11L3 6 3.7 5.3 8 9.6 12.3 5.3 13 6z"></path></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bx--form-item">
                    <label for="product-price" class="bx--label">Product Price (in USD)</label>
                    <input id="product-price" name="product-price" type="number" class="bx--text-input">
                </div>
                <div class="bx--form-item">
                    <label for="product-description" class="bx--label">Product Description</label>
                    <textarea id="product-description" class="bx--text-area" rows="4" cols="50" placeholder="Describe the product"></textarea>
                </div>
                <div class="bx--form-item">
                    <div class="bx--select">
                        <label for="select-id" class="bx--label">Product Category</label>
                        <select id="select-id" class="bx--select-input">
                            <option class="bx--select-option" disabled selected hidden>Choose an option</option>
                            <optgroup class="bx--select-optgroup" label="Tonic Food Ingredients 滋补食品">
                                <option class="bx--select-option" value="American ginseng 西洋参">American ginseng 西洋参</option>
                                <option class="bx--select-option" value="Sea cucumber 海参">Sea cucumber 海参</option>
                                <option class="bx--select-option" value="Edible bird's nest 燕窝">Edible bird's nest 燕窝</option>
                                <option class="bx--select-option" value="Ganoderma lucidum 灵芝">Ganoderma lucidum 灵芝</option>
                                <option class="bx--select-option" value="Caterpillar fungus 冬虫夏草">Caterpillar fungus 冬虫夏草</option>
                                <option class="bx--select-option" value="Velvet antler 鹿茸">Velvet antler 鹿茸</option>
                                <option class="bx--select-option" value="Fish maw 花胶">Fish maw 花胶</option>
                                <option class="bx--select-option" value="Panax ginseng 人参">Panax ginseng 人参</option>
                            </optgroup>
                            <optgroup class="bx--select-optgroup" label="TCM Dietary Supplements 中药保健品">
                                <option class="bx--select-option" value="Spleen and Stomach 补脾和胃">Spleen and Stomach 补脾和胃</option>
                                <option class="bx--select-option" value="Kidney and Energy 补肾固精">Kidney and Energy 补肾固精</option>
                                <option class="bx--select-option" value="Blood and fetus补血安胎">Blood and fetus补血安胎</option>
                                <option class="bx--select-option" value="Liver and temper 疏肝理气">Liver and temper 疏肝理气</option>
                                <option class="bx--select-option" value="Lung and phlegm 理肺祛痰">Lung and phlegm 理肺祛痰</option>
                            </optgroup>
                            <optgroup class="bx--select-optgroup" label="Others 其他">
                                <option class="bx--select-option" value="Raw herbs 中草药">Raw herbs 中草药</option>
                                <option class="bx--select-option" value="Herbal extract 中药精华">Herbal extract 中药精华</option>
                                <option class="bx--select-option" value="TCM supplementary products 中医辅助产品">TCM supplementary products 中医辅助产品</option>
                            </optgroup>
                        </select>
                        <svg focusable="false" preserveAspectRatio="xMidYMid meet" style="will-change: transform;" xmlns="http://www.w3.org/2000/svg" class="bx--select__arrow" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 11L3 6 3.7 5.3 8 9.6 12.3 5.3 13 6z"></path></svg>
                    </div>
                </div>
                <div class="bx--form-item">
                    <strong class="bx--file--label">Product photos</strong>
                    <input type="file" id="file" name="file" multiple>
                </div>
                <div class="bx--form-item">
                    <button class="bx--btn bx--btn--primary" type="submit">Submit</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/view-submissions')
def view_submissions():
    return render_template_string("""
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                width: 100%;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            @media (max-width: 600px) {
                body {
                    padding: 20px;
                    height: auto;
                }
                .container {
                    box-shadow: none;
                    border-radius: 0;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Submitted Names</h1>
            {% for submission in submissions %}
                <p>{{ submission }}</p>
            {% endfor %}
            <a href="/">Back to Form</a>
        </div>
    </body>
    </html>
    """, submissions=get_submissions())

def get_submissions():
    if os.path.exists('submissions.txt'):
        with open('submissions.txt', 'r') as file:
            return file.readlines()
    return []

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['product-name']
    
    with open('submissions.txt', 'a') as file:
        file.write(name + '\n')

    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist("file")
    if not files:
        return 'No files uploaded'
    for file in files:
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return f"Hello, {name}! Your name and file have been saved."

@app.route('/.well_known/apple-developer-merchantid-domain-association')
def apple_pay_verification():
    return send_file('/Users/kewengu/Downloads/apple-developer-merchantid-domain-association')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(host='0.0.0.0', port=5001, debug=True)

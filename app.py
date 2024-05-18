from flask import Flask, render_template, request
import pickle
import numpy as np

with open('popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)

with open('pt.pkl', 'rb') as f:
    pt = pickle.load(f)

with open('books.pkl', 'rb') as f:
    books = pickle.load(f)

with open('similarity_scores.pkl', 'rb') as f:
    similarity_scores = pickle.load(f)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if len(pt.index) > 0:
        index = np.where(pt.index == user_input)[0]
        if len(index) > 0:
            similar_items = sorted(list(enumerate(similarity_scores[index[0]])), key=lambda x: x[1], reverse=True)[1:5]

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                data.append(item)

            print(data)
            return render_template('recommend.html', data=data)
        else:
            return render_template('error.html', message="User input not found")
    else:
        return render_template('error.html', message="Index is empty")


if __name__ == '__main__':
    app.run(debug=True)
# Define error handlers for 404 and 500 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message="Server error"), 500

import pandas as pd
from wordcloud import WordCloud

# Open the Excel file
file_path = 'parties_topics.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(file_path)

# Display the DataFrame
print(df)
import matplotlib.pyplot as plt

"""
# Combine all words in the columns issue1, issue2, and issue3 into a list
words = df['Issue1'].dropna().tolist() + df['Issue2'].dropna().tolist() + df['Issue3'].dropna().tolist()

# Join the list into a single string
text = ' '.join(words)

# Create a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Create a word cloud with shading according to the number of times a word appears
wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
"""


# Create a cumulative word cloud for each row in the DataFrame
all_words = ' '.join(df['Issue1'].dropna().tolist() + df['Issue2'].dropna().tolist() + df['Issue3'].dropna().tolist())
cumulative_words = ''
cumulative_parties = []
counter = 0

# Generate the initial word cloud with all words to fix the layout
initial_wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False, contour_color='black', contour_width=1, color_func=lambda *args, **kwargs: "green").generate(all_words)
layout = initial_wordcloud.layout_

for index, row in df.iterrows():
    cumulative_words += ' '.join([str(row['Issue1']), str(row['Issue2']), str(row['Issue3'])]) + ' '
    cumulative_parties.append(str(row['Party']))
    counter += 1
    
    # Generate the word cloud with all words using the fixed layout
    wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False, random_state=None, contour_color='black', contour_width=1, mode="RGBA", color_func=lambda *args, **kwargs: "green").generate_from_frequencies(initial_wordcloud.words_)
    wordcloud.layout_ = layout
    
    # Recolor the word cloud to make words that occur less more transparent
    #inten = 0.2
    #cumulative_word_freq = WordCloud().process_text(cumulative_words)
    #if counter != 11:
    #    wordcloud = wordcloud.recolor(color_func=lambda word, font_size, position, orientation, random_state=None, mode="RGBA", **kwargs: f"rgba(0, 128, 0, 100)")

    # Recolor the word cloud to shade words that occur more often in the cumulative list darker
    cumulative_word_freq = WordCloud().process_text(cumulative_words)
    if counter != 11:
        wordcloud = wordcloud.recolor(color_func=lambda word, font_size, position, orientation, random_state=None, mode="RGBA", **kwargs: f"rgba(0, 128, 0, {int(30 + cumulative_word_freq.get(word, 0) * 255/10)})")
    else:
        wordcloud = wordcloud.recolor(color_func=lambda word, font_size, position, orientation, random_state=None, mode="RGBA", **kwargs: f"rgba({int(255*(word == 'immigration'))}, {int(128*(word != 'immigration'))}, 0, {int(30 + cumulative_word_freq.get(word, 0) * 255/10)})")    

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'wordcloud_{counter}.png')
    plt.show()


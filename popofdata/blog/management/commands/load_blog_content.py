from django.core.management.base import BaseCommand
from blog.models import Category, Post, SiteSettings
from datetime import date


class Command(BaseCommand):
    help = 'Load initial blog content from Pop-of-Data'

    def handle(self, *args, **options):
        # Delete existing data to reload
        Post.objects.all().delete()
        SiteSettings.objects.all().delete()

        # Create Site Settings - using local static images
        SiteSettings.objects.create(
            site_name='Pop-of-Data',
            tagline='Data Science for Pop Culture',
            hero_image='/static/images/pop_of_data.jpg',
            favicon='/static/images/smallpop.png',
            author_name='Audrey Taylor-Akwenye',
            author_title='Data Scientist, Educator, Entrepreneur',
            author_image='/static/images/IMG_0601.jpg',
            twitter_url='https://twitter.com/audreyakwenye',
            instagram_url='https://www.instagram.com/audreyakwenye',
            github_url='https://github.com/audreyakwenye',
        )
        self.stdout.write(self.style.SUCCESS('Created site settings'))

        # Create Categories
        music, _ = Category.objects.get_or_create(name='Music', slug='music')
        media, _ = Category.objects.get_or_create(name='Media', slug='media')
        tech, _ = Category.objects.get_or_create(name='Tech', slug='tech')
        trends, _ = Category.objects.get_or_create(name='Trends', slug='trends')
        self.stdout.write(self.style.SUCCESS('Created categories'))

        # Create Beyonce Post - using local static images
        beyonce_content = '''
<p>Since 16 in her stilettos she's been strutting her stuff and producing original songs in all genres from Country to Rock! With the recent release of her Netflix documentary "Homecoming", fans have been looking back over the two-decade career of the Queen herself. Below is a breakdown of the major topic patterns that can be found throughout her songs.</p>

<p>Latent Dirichlet Allocation (LDA) is a model that analyzes large documents of text and then drills down on major topics. I used the Gensim package to analyze all Beyonce song lyrics including her latest album with her hubby Jay Z.</p>

<p>I was able to compile all the lyrics for Beyonce from a larger dataset of over 380,000 lyrics from Metro Lyrics. Because the dataset was too large, I had to host the csv file on AWS S3. This gave me a total of 137 songs.</p>

<div class="video-container">
    <iframe src="https://www.youtube.com/embed/fB8qvx0HOlI" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

<p>Using pyLDAvis, we can see the 30 most salient terms from Beyonce's Lyrics.</p>

<h2>The Code</h2>

<h3>Build Bigrams and Trigrams</h3>
<p>Bigrams look at the two words before and after a word to pull out some context. Trigrams do the same but for the three words before and after. We also have to remove stop words. These are commonly used words that don't really add to the context of a text.</p>

<pre><code># Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc))
             if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc
                          if token.pos_ in allowed_postags])
    return texts_out</code></pre>

<h3>Remove Stop Words</h3>
<p>Next we create the corpus. We use doc to bag-of-words to encode each word in the lyrics.</p>

<pre><code>id2word = corpora.Dictionary(data_lemmatized)
texts = data_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]
[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]</code></pre>

<h3>Run the LDA Model</h3>
<p>Using gensim, I build the lda_model which will create 10 topics. The 10 passes means the lda model will go through the lyrics 10 times to improve the Coherence Value.</p>

<pre><code>lda_model = gensim.models.ldamodel.LdaModel(
    corpus=corpus,
    id2word=id2word,
    num_topics=10,
    random_state=100,
    update_every=1,
    chunksize=100,
    passes=10,
    alpha='auto',
    per_word_topics=True
)</code></pre>

<h3>Get LDA Model Coherence Scores</h3>
<p>Next we use LDA Mallet to generate coherence scores for our lda model. After working around to get the optimal number of topics, we get 14 topics that are shown below.</p>

<pre><code># Show Topics
pprint(ldamallet.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet = CoherenceModel(
    model=ldamallet,
    texts=data_lemmatized,
    dictionary=id2word,
    coherence='c_v'
)
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('\\nCoherence Score: ', coherence_ldamallet)</code></pre>

<h3>Interpret the Results</h3>
<p>Interpreting the topics is actually the most difficult part of topic modeling because it takes a little domain knowledge. My interpretation is below:</p>

<div class="topic-list">
    <h3>Beyonce's 14 Song Topics</h3>
    <div class="topic-item"><strong>0: "I'm a Hustler"</strong> — big, back, talk, upgrade, good, hustler, call, strong, tough, diva</div>
    <div class="topic-item"><strong>1: "I will fight you"</strong> — hand, hold, man, daddy, side, smack, air, care, said_shoot, put</div>
    <div class="topic-item"><strong>2: "I'm independent"</strong> — girl, freedom, wanna, make, fall, kind, baby, dress, daddy, club</div>
    <div class="topic-item"><strong>3: "I rep my crew"</strong> — make, pull, leave, real, friend, die, boss, bad, gon, jump</div>
    <div class="topic-item"><strong>4: "Girl Power"</strong> — girl, run, world, motha, catch, boy, pray, bring, play, check</div>
    <div class="topic-item"><strong>5: "I slay"</strong> — slay, make, good, lady, flawless, ride, teach, rock, bitch, hard</div>
    <div class="topic-item"><strong>6: "Don't Play Me"</strong> — work, hurt, ring, lie, money, beautiful, give, back, start, cry</div>
    <div class="topic-item"><strong>7: "S*xual Relations"</strong> — turn, cherry, feel, til, wait, stand, morning, home, time, stop_lov</div>
    <div class="topic-item"><strong>8: "I'm the Queen"</strong> — life, town, care, live, bow, ground, forget, watch, man</div>
    <div class="topic-item"><strong>9: "Leave Something Behind"</strong> — baby, put, top, time, day, make, boy, whatev, stay, immortal</div>
    <div class="topic-item"><strong>10: "I like to Party"</strong> — wanna, tonight, babe, body, baby, show, rock, feel, move, dance</div>
    <div class="topic-item"><strong>11: "I'm crazy"</strong> — love, crazy, baby, break, feel, hop, touch, make, jealous, promise</div>
    <div class="topic-item"><strong>12: "You cheat, You Crazy"</strong> — good, hear, put, lose, wanna, thing, time, face, boy, thinking_bout</div>
    <div class="topic-item"><strong>13: "But I Love you"</strong> — love, night, light, baby, kiss, long, rub, feel, boy, sweet</div>
</div>

<h2>Conclusion</h2>
<p>Through topic modeling, we can see that Beyonce's music covers a wide range of themes from empowerment and independence to love and relationships. Her most common topics center around being strong, independent, and in control.</p>
'''

        Post.objects.create(
            slug='beyonce-topic-modeling',
            title='Beyonce Topic Modeling',
            featured_image='/static/images/beyonce.jpeg',
            excerpt='Using LDA topic modeling to analyze Beyonce song lyrics',
            content=beyonce_content,
            category=music,
            author='Audrey Taylor-Akwenye',
            published_date=date(2019, 4, 21),
        )
        self.stdout.write(self.style.SUCCESS('Created Beyonce post'))

        # Create QaiQai Post - using local static images
        qaiqai_content = '''
<p>Natural Language processing is a Machine Learning application where we can train a computer to analyze and attempt to interpret human-readable text. Unfortunately, the underlying language of computers is math, so there needs to be a method to translate human-readable text into math. Word to Vector is a method to do just that. I have used Basilica to create Word2Vec embeddings of hundreds of tweets to solve one of the biggest social media mysteries of the last year….. <strong>WHO IS @REALQAIQAI?</strong></p>

<p>In mid-August 2018, a new account for @RealQaiQai sent her first tweet. This alone doesn't seem odd as more than half a million users tweet daily. However, Qai Qai is a small African American baby doll who's the partner-in-crime to Olympia Ohanian, the daughter of Serena Williams and Alexis Ohanian. The @RealQaiQai has since become America's favorite doll with over 20k Twitter followers.</p>

<div class="gallery">
    <img src="/static/images/2.png" alt="Alexis Ohanian">
    <img src="/static/images/3.png" alt="Serena Williams">
    <img src="/static/images/4.png" alt="Olympia Ohanian">
    <img src="/static/images/5.png" alt="Qai Qai">
</div>

<p>The world became obsessed with the blossoming relationship between Serena and Alexis in 2018, when the couple announced their engagement. In September, Olympia was born, and by August, the new parents were grandparents. Qai Qai the Doll became an instant hit on Twitter and Instagram with her catchy clap backs and beautiful pics from a doll's point of view. However, unlike Olympia's Twitter profile which clearly explains that both mom and dad manage the account, the adoring fans of @RealQaiQai have no idea which superstar parent is the author behind the account.</p>

<div class="video-container">
    <iframe src="https://www.youtube.com/embed/ge3NCQNBDqg" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

<p>Many believe it's Alexis, the founder of Reddit, because of his background in tech and love of social media. Using Natural Language Processing and a Logistic Regression model, we can finally put this mystery to bed.</p>

<h2>The Code</h2>

<h3>Using Twitter API</h3>
<p>The first step to solving this 'who done it' is to pull tweet history from @alexisohanian, @serenawilliams, and @RealQaiQai. This was done through Twitter's developer API.</p>

<pre><code># User 1
username = "serenawilliams"
number_of_tweets=200
tweets = TWITTER.user_timeline(username, count=200, exclude_replies=True,
                               include_rts=False, tweet_mode='extended')
tmp=[]
tweets_for_csv = [tweet.full_text for tweet in tweets]
for j in tweets_for_csv:
    tmp.append(j)</code></pre>

<h3>Word to Vector with Basilica</h3>
<p>Once we have all the tweets, we use Basilica to convert words to vectors. This process turns a word into a collection of numbers that can be understood by the computer. Once the words are vectors, the computer can analyze the speech patterns, word usage, and sentiment of the tweets.</p>

<pre><code>user1 = []
for tweet in tweets:
    user1_embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
    user1.append(user1_embedding)</code></pre>

<h3>Apply Logistic Regression Model</h3>
<p>We then feed all this analysis into a logistic regression model. We train the computer to identify which tweets were written by Serena and which were written by Alexis. After training, we fed the word to vector information from QaiQai. The logistic regression model can then predict which tweet was more similar to Serena's tweets, and which were more like Alexis.</p>

<pre><code>import numpy as np
from sklearn.linear_model import LogisticRegression

embeddings = np.vstack([user1, user2])
labels = np.concatenate([np.ones(len(user1)),
                         np.zeros(len(user2))])
log_reg = LogisticRegression().fit(embeddings, labels)</code></pre>

<h3>Predict Parent Author</h3>
<p>And finally, we can compare the predictions of each tweet from @RealQaiQai to see which parent was predicted more often. Drum roll please…..</p>

<pre><code>preds = []
for tweets in tmp3:
    tweet_embedding = BASILICA.embed_sentence(tweets, model='twitter')
    prediction = log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
    preds.append(prediction)</code></pre>

<div class="conclusion">
    <h3>Conclusion</h3>
    <img src="/static/images/serenagraph.png" alt="Results Graph" class="conclusion-img">
    <p><strong>The parent behind @RealQaiQai is roughly twice as likely to be Serena than Alexis.</strong> The results don't definitively say that only Serena Williams is the author of @RealQaiQai, but it looks likely.</p>
</div>
'''

        Post.objects.create(
            slug='whos-the-realqaiqai',
            title="Who's the @RealQaiQai?",
            featured_image='/static/images/qaiqai.png',
            excerpt='Using NLP to discover who manages the famous doll Twitter account',
            content=qaiqai_content,
            category=media,
            author='Audrey Taylor-Akwenye',
            published_date=date(2019, 4, 8),
        )
        self.stdout.write(self.style.SUCCESS('Created QaiQai post'))

        # Create Launch/Founder University Post - using local static images
        launch_content = '''
<p>6 months ago, I attended Founder University, a free workshop hosted in San Francisco by Jason Calacanis. It was my first time in San Francisco and the experience completely changed the trajectory of my life. To explain how, I have to go back a few months before.</p>

<p>In July of 2018, I launched my edtech startup Schoolio. The platform was geared towards low-cost private schools in developing countries to help them manage their student data and use machine learning to improve student outcomes. I took the experiences and systems I developed while building a low-cost private school in Namibia and went looking for a developer to help me automate my pedagogical techniques. Four months later, I had paid out over $30,000 USD to a developer consultant who didn't have the skills to fully flesh out the "V" in my MVP. I was out of money and still didn't have a proof of concept. My company was definitely circling the drain.</p>

<p>I decided to part ways with the consultant and find a more skilled (and probably more expensive) consultancy firm. I tried finding a technical co-founder but convincing a stranger to build for free was a hard sell and I didn't have the funding to commit to bringing on a full-time employee. So, working with consultants looked like my only option. I found a consultancy firm that focused on machine learning and after a few video chats, I was presented with their quote:</p>

<blockquote>$60,000 USD with a 4-month development timeline.</blockquote>

<p>The problem with the quote was 1. I didn't have 60k and 2. What was I supposed to do for 4 months while I waited on the product to be developed?</p>

<h2>Then I went to Founder University...</h2>

<div class="instagram-placeholder">
    <div class="ig-icon"><i class="fa fa-instagram"></i></div>
    <p>View this post on Instagram</p>
    <p><a href="https://www.instagram.com/p/Bp7h31vh4SG/" target="_blank">A post shared by Audrey Taylor Akwenye (@audreyakwenye)</a></p>
    <p style="color: #888; font-size: 12px;">Nov 8, 2018</p>
</div>

<p>These were the challenges I had to overcome when I was accepted to Founder University. I shared these problems in discussions with the other workshop participants as well as the panelists. During the three days, I saw a pattern emerge:</p>

<ul>
    <li>Companies with technical founders had challenges like gaining customers, building a brand, and/or perfecting sales strategy</li>
    <li>Companies with non-technical founders all had the same challenge — how to get technical talent.</li>
</ul>

<p>Frustrated by what this pattern meant for my company, I asked Jason, "What do you do if you need money to build the MVP, but you need the MVP to get the money?" He said very frankly (I'm paraphrasing his frankness) —</p>

<blockquote>If you can't figure out how to get your product to market, you don't deserve to be a founder.</blockquote>

<p>This statement was really an "Aha" moment for me. In essence, he was urging us to get the product developed by any means necessary. I want to disclaim that "by any means necessary" is different for everyone. I'm not saying the path I took for my "by any means necessary" is the only or even the best way. It's merely the choices I made.</p>

<p>I looked at the 60k quote I received and thought:</p>

<div class="key-points">
    <h4>"What is needed to build my product?"</h4>
    <p><strong>1. Knowledge/Skill</strong></p>
    <p><strong>2. Time</strong></p>
    <p><strong>3. Money</strong></p>
</div>

<p>Currently, I only had the time. I needed either the knowledge/skill or the money to pay for the knowledge/skill. With that, I knew what I needed to do.</p>

<p>Instead of spending another year trying to find the money to hire someone to build my site, I would spend that time acquiring the knowledge to do it myself. 4 months and 60k sound like a great start to an education. Before that moment, I had never once considered obtaining any formal education in tech. But now, I saw studying as the best investment for my business. It was the only guaranteed way I saw getting my product to market.</p>

<p>That's when I decided to join Lambda School in the Data Science program. It also helped that I didn't have to pay up front. My thought process was that one of two things would happen. Either, I would acquire the skills to relaunch Schoolio and then I could hire myself to pay back my ISA or Schoolio was destined to fail and at least I would be able to get a job afterward.</p>

<p>Now 6 months later, I'm relaunching Schoolio with a pivot now using AI to support High School students in Africa and I was able to write all the code, structure every database, and build every algorithm. Becoming my own technical co-founder has helped me see the benefit of having a strong technical founding team. Once again, this is what I felt was right for my company and that doesn't mean that every tech company has to have a technical cofounder. For me, becoming a technical founder allowed me to:</p>

<div class="benefit-card">
    <h3>Become more Agile</h3>
    <p>Building my own tech means that I can change and iterate quickly as I get feedback from my team or customers. Working with a consultant means even little changes can take weeks.</p>
</div>

<div class="benefit-card">
    <h3>Become more Defensible</h3>
    <p>I am able to develop tech that can implement new techniques or applications making me more defensible in the market. Outsourcing development means I would probably only get something that has been developed before.</p>
</div>

<div class="benefit-card">
    <h3>Know what's possible</h3>
    <p>I don't plan on being the only developer on the team forever but as CEO, I'm now able to have a better understanding of what is possible and on what timeline. This helps me lead and manage a team of developers in the future.</p>
</div>

<p>So now 6 months later, I've begun my journey as a Data Scientist. Because of this I'm exploring so many ways Schoolio can use AI to improve Global Education. All of this because of the experience and advice I received at Founder University.</p>
'''

        Post.objects.create(
            slug='how-founder-university-changed-my-life',
            title='How Founder University Changed My Life',
            featured_image='/static/images/Founder_University.png',
            excerpt='My journey from non-technical founder to data scientist',
            content=launch_content,
            category=tech,
            author='Audrey Taylor-Akwenye',
            published_date=date(2019, 5, 1),
        )
        self.stdout.write(self.style.SUCCESS('Created Founder University post'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all blog content!'))

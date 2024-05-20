from analyzer import Analyzer


test_posts = ['I have been great lately. I got a new job. and i am getting married', 'last night was awful i was depressed and was feeling down', 'How to play football']
test_results = Analyzer().analyze(test_posts)
print(list(zip(test_posts, test_results[0], test_results[1], test_results[2])))

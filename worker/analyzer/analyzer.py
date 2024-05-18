from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import tensorflow as tf
import logging


logger = logging.getLogger("internal_analyzer_logger")

class Analyzer:
    def __init__(self, *args, **kwargs):
        logger.info("Initializing Analyzer...")

        # load model
        logger.info("   Loading model...")
        self.model = load_model("model/model.keras")

        # load json tokenizer
        logger.info("   Loading tokenizer...")
        with open('model/tokenizer.json', 'r') as file:
            content = file.read()
            if not content:
                logger.error("  Error loading tokenizer. File is empty. Exiting...")
                raise Exception("Error loading tokenizer. File is empty.")
        self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(content)

    def prepare_data(self, posts):
        logger.info("Preparing data...")
        logger.info("   Tokenizing posts...")
        sequences = self.tokenizer.texts_to_sequences(posts)
        logger.info("   Padding sequences...")
        padded_sequences = pad_sequences(sequences, maxlen=50)
        return padded_sequences

    def predict(self, posts):
        data = self.prepare_data(posts)
        logger.info("Predicting...")
        return self.model.predict(data)

    def label_results(self, results):
        logger.info("Labeling results...")
        result_encoded_classes = [1 if result > 0.5 else 0 for result in results]
        result_classes = ["Suicidal" if result == 1 else "Non Suicidal" for result in result_encoded_classes]
        return result_encoded_classes, result_classes

    def analyze(self, posts):
        results = self.predict(posts)
        return self.label_results(results)




if __name__ == "__main__":
    analyzer = Analyzer()
    posts = ["I am feeling so sad", "I am feeling happy"]
    print(analyzer.analyze(posts))
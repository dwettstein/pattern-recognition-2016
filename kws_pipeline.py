import numpy as np

from ip import doc_processor
from search import plot_accuracy
from search.kws import KWS


# Process the images and generate a feature map
doc_processor.main()

# process the logs, do some plots and stdout
plot_accuracy.main()

# Load training and validation data
knn = KWS()
knn.load_train_and_valid()

# Get one single page from the validation data
index = np.array([['300', '301'].count(x.doc_id) > 0 for x in knn.valid.coords], dtype=bool)
dataset = knn.valid.subset(index)

# Search
knn.set_data(dataset)
knn.create_index()
knn.search_word('the')

import numpy as np
import tensorflow as tf


def tensorize_labeled_spans(tuples, label_dict):
  if len(tuples) > 0:
    starts, ends, labels = zip(*tuples)
  else:
    starts, ends, labels = [], [], []

  if label_dict:
    return np.array(starts), np.array(ends), np.array([label_dict.get(c, 0) for c in labels])

  return np.array(starts), np.array(ends), np.array(labels)


# FIXME
def tensorize_srl_relations(tuples, label_dict, filter_v_args):
  # Removing V-V self-loop.
  if filter_v_args: 
    filtered_tuples = [t for t in tuples if t[-1] not in ["V", "C-V"]]
  else:
    filtered_tuples = [t for t in tuples if t[-1] != "V"]
    # filtered_tuples = tuples
  #print("input_utils: ", filtered_tuples)
  if len(filtered_tuples) > 0:
    heads, starts, ends, labels = zip(*filtered_tuples)
  else:
    heads, starts, ends, labels = [], [], [], []
  #print("heads, starts, ends, labels: ", heads, starts, ends, labels)
  return (np.array(heads), np.array(starts), np.array(ends),
          np.array([label_dict.get(c, 0) for c in labels]))


def get_all_predicates(tuples):
  if len(tuples) > 0:
    predicates, _, _, _ = zip(*tuples)
  else:
    predicates = []
  return np.unique(predicates)
  

def load_lm_embeddings_for_sentence(lm_file, lm_layers, lm_size, doc_key, sent_key):
  """ Load LM embeddings for given sentence.
  """
  if lm_file is None:
    return np.zeros([0, lm_size, lm_layers])  # FIXME: dimensions are wrong? Num. words, ...
  file_key = doc_key.replace("/", ":")
  group = lm_file[file_key]
  if sent_key is not None:
    sentence = group[sent_key][...]
  else:
    sentence = group[...]
  return sentence.transpose(1, 2, 0)


def pad_batch_tensors(tensor_dicts, tensor_name):
  """
  Args:
    tensor_dicts: List of dictionary tensor_name: numpy array of length B.
    tensor_name: String name of tensor.
  
  Returns:
    Numpy array of (B, ?)
  """
  #print("tensor_dicts: ", tensor_dicts)
  #print("tensor_name: ", tensor_name)
  #print("pad_batch_tensors")
  #print("tensor_dicts: ", tensor_dicts)
  #print("tensor_name: ",tensor_name)
  batch_size = len(tensor_dicts)
  #print("batch_size :", batch_size)
  tensors = [np.expand_dims(td[tensor_name], 0) for td in tensor_dicts]
  shapes = [list(t.shape) for t in tensors] 
  #print("originalshapes: ",shapes)
  # Take max shape along each dimension. 
  #print("zip: ",list(zip(*shapes)))
  max_shape = np.max(list(zip(*shapes)), axis=1)
  #print("shapes: ",shapes)
  #print("max_shape: ",max_shape)
  #print("t_shape[0].shape: ",tensors[0].shape)
  #print("t_shape[1].shape: ",tensors[1].shape)
  #print("max_shapes: ",max_shapes)
  #print tensor_name, batch_size, tensors[0].shape, max_shape
  zeros = np.zeros_like(max_shape)
  padded_tensors = [np.pad(t, list(zip(zeros, max_shape - t.shape)), "constant") for t in tensors]
  #print(padded_tensors)
  return np.concatenate(padded_tensors, axis=0)


def populate_sentence_offset(examples):
  # Compute sentence offset (that share the same doc key), because of LM embedding formatting difference.
  prev_doc_key = "XXX"
  sent_offset = 0
  for example in examples:
    doc_key = example["doc_key"][:example["doc_key"].rfind("_")]
    if doc_key != prev_doc_key:
      prev_doc_key = doc_key
      sent_offset = 0
    example["sent_offset"] = sent_offset
    sent_offset += len(example["sentences"])


def split_srl_labels(srl_labels, include_c_v):
  adjunct_role_labels = []
  core_role_labels = []
  for label in srl_labels:
    if "AM" in label or "ARGM" in label:
      adjunct_role_labels.append(label)
    elif label != "V" and (include_c_v or label != "C-V"):
      core_role_labels.append(label)
  return adjunct_role_labels, core_role_labels




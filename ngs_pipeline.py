import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from Bio import SeqIO

# Load NGS data (FASTA/FASTQ format)
def load_ngs_data(file_path):
    sequences = []
    for record in SeqIO.parse(file_path, "fasta"):
        sequences.append(str(record.seq))
    return sequences

# Preprocess sequences (one-hot encoding)
def preprocess_sequences(sequences, max_length=100):
    encoded_seqs = []
    for seq in sequences:
        encoded_seq = []
        for nucleotide in seq[:max_length]:
            if nucleotide == 'A':
                encoded_seq.append([1, 0, 0, 0])
            elif nucleotide == 'T':
                encoded_seq.append([0, 1, 0, 0])
            elif nucleotide == 'C':
                encoded_seq.append([0, 0, 1, 0])
            elif nucleotide == 'G':
                encoded_seq.append([0, 0, 0, 1])
            else:
                encoded_seq.append([0, 0, 0, 0])  # Unknown nucleotide
        # Pad sequences shorter than max_length
        while len(encoded_seq) < max_length:
            encoded_seq.append([0, 0, 0, 0])
        encoded_seqs.append(encoded_seq)
    return np.array(encoded_seqs)

# Build a simple deep learning model
def build_model(input_shape):
    model = Sequential([
        Dense(128, activation='relu', input_shape=input_shape),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')  # Binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Main function
def main():
    # Input file path
    input_file = "data/sample.fasta"
    
    # Load and preprocess data
    sequences = load_ngs_data(input_file)
    X = preprocess_sequences(sequences)
    y = np.random.randint(2, size=len(sequences))  # Placeholder for labels
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build and train the model
    model = build_model((X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
    
    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()

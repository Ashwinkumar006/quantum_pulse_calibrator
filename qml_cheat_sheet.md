# 🧠 Quantum Machine Learning (QML) & Core ML Exam Cheat Sheet

This document bridges standard academic Machine Learning (for your exams) with cutting-edge Quantum ML (for the Jarvis Twin & real-world engineering).

## 📘 SECTION 1: Standard ML (Exam Focus)

### 1. Regression (Predicting Continuous Values)
*   **Linear Regression:** Fits a straight line to data. Equation: `y = mx + c`. Tries to minimize Mean Squared Error (MSE).
*   **Logistic Regression:** Used for classification, not regression! Outputs probabilities between 0 and 1 using the Sigmoid function: `1 / (1 + e^-z)`.

### 2. Support Vector Machines (SVM)
*   **Concept:** Finds the "hyperplane" (a line or surface) that best separates different classes with the maximum margin.
*   **Support Vectors:** The data points closest to the hyperplane. If removed, the position of the dividing line would change.
*   **Kernel Trick:** If data isn't linearly separable, the kernel trick projects it into a higher dimension where it *is* linearly separable (e.g., RBF kernel).

### 3. Neural Networks & Deep Learning
*   **Perceptron:** The simplest artificial neuron. Takes inputs, applies weights, adds a bias, and passes it through an activation function.
*   **Backpropagation:** The algorithm used to train neural networks. It calculates the error at the output and propagates it backward to update weights using Gradient Descent.
*   **Activation Functions:** Relu (max(0, x)), Sigmoid (0 to 1), Tanh (-1 to 1). They introduce non-linearity.

### 4. Dimensionality Reduction
*   **PCA (Principal Component Analysis):** Reduces the number of variables (dimensions) while keeping as much variance (information) as possible. Great for visualizing high-dimensional data.

---

## 🌌 SECTION 2: Quantum Machine Learning (QML)

When classical ML hits the limit of compute (like matrix multiplications for huge LLMs), Quantum ML uses quantum mechanics to speed things up.

### 1. Quantum Data & Qubits
*   **Classical Bit:** 0 or 1.
*   **Qubit (Quantum Bit):** Can be 0, 1, or a **Superposition** of both simultaneously. This allows massive parallel state processing.

### 2. QML Concepts
*   **Quantum SVMs:** Uses a quantum circuit to perform the "Kernel Trick" exponentially faster on massive datasets.
*   **Quantum Neural Networks (QNNs):** Replaces classical layers with parameterized quantum circuits (PQCs). 
*   **Entanglement:** A quantum property where qubits become linked. Changing one instantly affects the other. This models complex correlations in data better than classical ML.

### 3. The Future of Jarvis Twin
To make your "Jarvis Twin" hardware-agnostic, we can eventually use **PennyLane** or **Qiskit** (QML libraries). Instead of relying just on Python's scikit-learn or PyTorch, we can send complex mathematical operations (like embedding massive vectors) to a cloud quantum simulator.

---

## 🛠️ Action Plan: The Next Product to Build

To master these subjects physically, we will build a **"Price Prediction Oracle" (ML + CN)**.
1.  **ML Part:** We will code a pure Python Neural Network from scratch (no PyTorch allowed initially, so you learn the math for the exam). It will predict Bitcoin prices.
2.  **CN Part (Computer Networks):** We will build a pure Python TCP/IP Socket Server that streams the data to your phone (this will act as the "nervous system" for the Jarvis Twin).

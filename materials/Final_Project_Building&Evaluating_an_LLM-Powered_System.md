# Final Project: Building & Evaluating an LLM‑Powered System

1. Goal
For the final project, you will design, build, and evaluate a small but meaningful system using large language models (LLMs).

The goal is not to train huge models from scratch, but rather to:

Use existing LLMs (via API or open-source models)
Write code to connect them to data or tasks
Design prompts or simple workflows
Evaluate how well your system works and where it fails
Ambitious projects that don’t fully "succeed" can still earn strong grades if they are well‑executed, evaluated honestly, and clearly explained.

2. Project Tracks (Choose One)
You must pick one main track; hybrids are possible only if the scope stays manageable.

Track A: LLM Application / Mini Tool
Build a small application that uses an LLM to help with a specific task.

Examples:

A study helper that answers questions based on a few chapters of course material
A writing assistant that rewrites text in a clearer, simpler, or more professional style
A simple code helper for one language and one type of task (e.g., explain Python errors)
A data explainer that summarizes small CSV files in plain language 
Requirements:

Define a clear user and task
e.g., "Intro stats students who want homework explanations"
Implement a working tool
Jupyter notebook, script, or simple UI (CLI or minimal web form is fine)
Use at least one LLM (API or open‑source)
Evaluate on a small but real set of inputs
e.g., 10–30 example questions/texts; can include simple user feedback
Include a short analysis of what the system does well and where it breaks
 

Track B: Prompt Design & Evaluation
Systematically experiment with different prompts and see how they affect an LLM's performance on a simple task.

Task ideas (high‑level):

Sentiment classification on product reviews
Topic classification (sports vs. tech vs. politics, etc.)
Math word problems or simple logic puzzles
Short‑answer grading (e.g., "Is this answer correct? Why or why not?")
Requirements:

Choose a task and find/build a small dataset
On the order of 100–300 examples is fine
Design different prompts that cover:
Each of zero‑shot, few‑shot, and chain‑of‑thought prompting
Various levels of specification for system and user messages
Various levels of specification for persona, task, constraints, and output
Run the LLM on your dataset with each prompt and compare results
Simple metrics: accuracy, or % correct, or rating scores
Present tables or simple plots summarizing the results
Do a brief error analysis on some incorrect outputs
Where do certain prompts help or hurt?
Track C: Retrieval-Augmented Question Answering (Mini-RAG)
Connect an LLM to a small set of documents and build a system that answers questions using those documents.

Examples:

Q&A over course materials (syllabus, assignments, lecture notes)
Q&A over a small curated set of articles/blog posts on one topic
FAQ bot for a club or small organization (using their website/FAQ text)
Requirements:

Build a small document collection
e.g., 10–50 short documents or pages (saved as text)
Implement a simple RAG pipeline
Some way to retrieve relevant document chunks
Send the question + retrieved text to the LLM
Compare at least:
LLM without retrieval (just ask the question)
LLM with retrieval
Evaluate on 20–30 realistic questions
Rate answers as correct / partially correct / incorrect, and note hallucinations
Provide example Q&A pairs showing where retrieval helps (or doesn’t)
Track D: Lightweight Fine‑Tuning / Adaptation
Adapt a small pre‑trained model (not a huge LLM) to a simple text task using a modest labeled dataset.

The goal is to get hands‑on practice with supervised learning on text.

Typical tools:

Python + Hugging Face transformers (or similar)
Small pre‑trained models (e.g., DistilBERT‑style classifiers, tiny encoder/decoder models)
JupyterHub / Jupyter Lab or equivalent
Examples:

Domain‑specific sentiment classifier (e.g., course evaluations, product reviews)
Helpdesk / FAQ intent classifier (billing vs. tech support vs. account access, etc.)
Short‑text feedback summarizer for simple one‑sentence summaries
Requirements:

Task & Dataset
Choose a clear supervised task (e.g. classification or short text generation).
Use a small labeled dataset, roughly:
Classification: ~300–2,000 labeled texts
Summarization: ~200–500 (input, summary) pairs
Split into train / validation / test (e.g., 70% / 15% / 15%).
Models
Start from a pre‑trained base model, not random initialization.
Fine‑tune it on your training data.
Optional: model also with a simple baseline (e.g., logistic regression with bag‑of‑words).
Training & Practicality
Keep the model small enough to train in a reasonable time on free/low‑cost compute.
Try at least one small variation in training setup (e.g., different number of epochs).
Evaluation
Use appropriate metrics:
Classification: accuracy/precision/recall/F1.
Summarization: basic automatic metric plus manual inspection.
Report results on the test set.
Analysis
Show a few concrete examples the model gets right and wrong.
Discuss:
What improved after fine‑tuning
Typical error patterns
Any signs of overfitting (e.g., training vs. validation performance)
 

3. Tools & Constraints
You are encouraged to use:

Python (Jupyter/Colab/VS Code)
LLMs via API (e.g., NRP, OpenAI, or other hosted services) or small open-source models
Common libraries (e.g., pandas, numpy, scikit-learn, matplotlib/seaborn, RAG/prompting libraries)
You are not required to:

Train large models from scratch
Use GPUs beyond what is provided by free resources (e.g., JupyterHub/Colab)
Design your project so it works with modest compute and reasonable time.

 

4. Deliverables
1) Project Proposal (≈1 page, PDF)
Due on Monday, May 18.

Include:

Track (A, B, C, or D) and working title
Task description and motivation (3–5 sentences)
Planned:
Model(s) and libraries/frameworks
Data (where it comes from; size; any labeling needed)
Evaluation plan (metrics, # of examples, any user feedback)
A simple backup plan if something doesn’t work
e.g., smaller dataset, simpler model, fewer features
2) Final Report (≈4–6 pages, PDF)
Suggested structure:

Introduction
What problem are you solving, and why is it interesting/useful?
What did you build or test?
Data & Setup
Data source(s), size, and any preprocessing/cleaning
Brief description of users/docs/tasks as needed
Methods
Models and prompts (or fine‑tuning setup)
System architecture or pipeline (diagrams encouraged)
For Track D: training setup and hyperparameters at a high level
Experiments & Results
Evaluation setup (metrics, number of examples, procedure)
At least one table and/or figure summarizing results
For RAG: with vs. without retrieval
For prompts: different prompt styles
For fine‑tuning: baseline vs. fine‑tuned model
Qualitative Analysis & Error Cases
Example inputs/outputs showing strengths and failures
Ethics & Limitations (short section)
Any privacy, bias, misuse, or safety concerns
Limitations of your data and methods
Conclusion & Future Work
Main takeaways and possible next steps
3) Code & Artifacts
Submit:

A zip file with:
Main notebooks/scripts
A short README explaining:
How to run your main experiment or demo
If your notebooks/scripts are not runnable with the JupyterHub environment, include how to set up the environment (e.g., requirements.txt)
Any small datasets you used/created, plus a brief description
Code does not have to be production‑grade, but it should be:

Organized (reasonable file structure)
Readable (basic comments and clear variable names)
4) Short Presentation (5–10 minutes)
A recorded presentation that covers:

Problem & motivation
What you built (system or experimental setup)
Key results (with at least one figure or table)
A short demo or example outputs
1–2 "lessons learned" about using LLMs / NLP models in practice
 

5. Example Project Ideas (By Track)
You are welcome to propose your own idea. The examples below show the right scope and flavor for each track.

Track A – LLM Application / Mini Tool
Email Tone Rewriter for Workplace Messages
Input: a draft email + desired tone ("more formal," "more friendly," "more concise").
Output: rewritten email, optionally with a short explanation of changes.
Evaluation: 10–20 sample emails rated for clarity and appropriateness of tone.
Quiz Question Generator from Short Readings
Input: a textbook paragraph or short article.
Output: a few multiple‑choice questions (correct answer + distractors).
Evaluation: check correctness of answers and have a few users attempt the quiz.
Simple Code Comment Generator for Intro Python
Input: short Python snippets (loops, conditionals, basic functions).
Output: line‑by‑line explanation or comments.
Evaluation: ask classmates/friends with basic Python to rate whether the explanations helped their understanding; look for incorrect explanations.
Track B – Prompt Design & Evaluation
Headline Rewriter for Different Audiences
Take ~50 news headlines.
Prompt the LLM to rewrite for: a 10‑year‑old child, general audience, and experts.
Compare different prompt styles.
Evaluation: ask a few people to rate clarity and appropriateness for each audience.
Product Review Summarizer and Sentiment Tagger
Dataset: ~50–100 product reviews.
LLM produces a 1–2 sentence summary plus a sentiment label (Positive/Neutral/Negative).
Compare outputs of different prompts (with examples).
Evaluate sentiment labels against your own labels and qualitatively inspect summaries.
Track C – Retrieval‑Augmented QA (Mini‑RAG)
Course Syllabus Q&A Bot
Documents: course syllabus + assignment descriptions.
System: RAG over these docs so students can ask “When is the final project due?”, etc.
Compare LLM alone vs. LLM + retrieval.
Evaluate answer correctness and hallucination rates on ~30–40 questions.
FAQ Bot for a Small Website or Club
Documents: pages and FAQs from a student club, meetup group, or small organization.
System: simple search + LLM answer generation.
Evaluation: create ~20–30 realistic user questions and compare accuracy with vs. without retrieval.
Track D – Lightweight Fine‑Tuning / Adaptation
Domain‑Specific Sentiment Classifier
Task: classify domain‑specific reviews (e.g., apps, restaurants, course evaluations) as Positive/Neutral/Negative.
Data: a few hundred labeled reviews (public or manually labeled).
Models:
Baseline: simple bag‑of‑words + logistic regression (optional but recommended).
Fine‑tuned: small pre‑trained classifier fine‑tuned on your data.
Evaluate accuracy on a test set and show review examples where fine‑tuning helps.
Helpdesk / FAQ Intent Classifier
Task: label short user questions by intent (e.g., Billing, Technical Issue, Account Access, General Info).
Data: ~300–800 short questions labeled with 5–10 intent categories.
Model: fine‑tune a small text classifier.
Evaluate overall accuracy and show a confusion matrix; analyze which intents are most often confused.
Short Feedback Summarizer for Course or Product Feedback
Task: turn short feedback paragraphs into one‑sentence summaries.
Data: ~200–500 (feedback, summary) pairs.
Baseline: LLM with a generic "summarize in one sentence" prompt.
Fine‑tuned model: small seq2seq model trained on your pairs.
Compare baseline vs. fine‑tuned summaries on a held‑out test set; manually inspect which is closer to your reference summaries.
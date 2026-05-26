# Final Project: Peer Review Completion

As part of the final project's Prototype Submission, you will automatically be assigned to anonymously review classmates' projects.  The goal is to help each other improve and to practice reading and evaluating LLM work critically and kindly.

Your job is not to be a harsh judge. Your job is to be a thoughtful, supportive colleague who gives specific, honest, and useful feedback.

1. What You Should Submit for Each Peer

For each project you review, you should provide:
Short summary (3–5 sentences)
Strengths (at least 3 concrete things they did well)
Suggestions for improvement (at least 3 specific, actionable suggestions)
Questions / clarifications (2–3 questions that could help them think deeper)
Overall impression (1–2 sentences: what you found most interesting or promising)
You should base your review on:
The written final report
Any figures/tables included
The presentation (if available at review time)
Description of the system or results
2. On Being Constructive

Constructive feedback = specific + respectful + focused on improvement.
Do:
Focus on the work, not the person:
"The evaluation section could be clearer if you separated results by dataset." rather than "You’re not good at writing evaluation."
Be specific, not vague:
"Figure 2 is hard to read because the labels overlap—this might be improved by increasing font size or simplifying the legend." rather than "Your figures need to be improved."
Balance praise and critique:
Point out what is working well and what could be improved.
Imagine you’re helping them prepare this for a public talk or a job interview.
Make actionable suggestions:
"You might add 1–2 example outputs in the Results section to make failures more concrete." rather than "Make the Results section better."
Don't:
Don’t criticize style without offering help:
Rather than write "Your writing is confusing," write "The Methods section is long and could be improved by adding subheadings like 'Data' and 'Model' to help readers navigate."
Don’t nitpick tiny things and ignore big ones:
It’s okay to mention typos, but focus first on clarity, methods, evaluation, and results.
Don’t compare people:
Avoid "Your project is worse than X’s" or "This is likely the best in the class." -- Just evaluate this work.
3. What to Look For

When writing your review, consider commenting on some of these areas:
Problem & Motivation
Is the task clearly described?
Do you understand why this project is interesting or useful?
Is the user or scenario (if applicable) clearly defined?
Data & Setup
Do you understand what data they used, where it came from, and how big it is?
Is the preprocessing, filtering, or labeling described clearly enough?
For Track D, is the train/validation/test setup clear?
Methods / System Design
Do you understand how the system works or how the experiments were run?
Are the prompts, models, and/or pipeline described clearly enough for you to roughly reproduce them?
Are diagrams or examples helpful? If not, how could they be improved?
Evaluation & Results
Are the metrics appropriate for the task?
Is it clear how many examples were evaluated and how?
Are tables/figures easy to read and interpret?
Do the results match the claims in the text?
Are there examples of outputs (good and bad)?
Discussion & Error Analysis
Do they discuss limitations and failure cases?
Do they offer any plausible explanations for why certain prompts/models worked better?
Do they mention potential ethical issues (bias, hallucinations, misuse) when appropriate?
Writing & Organization
Is the report easy to follow?
Are sections clearly labeled and logically ordered?
Are there places where a graph, table, or example would help?
You don’t have to comment on every one of these, but try to touch on several.
4. Suggested Structure for Each Review

You can roughly follow this template:
Summary (3–5 sentences)
Briefly restate the project in your own words:
What is the task?
What did they build or test?
What are the main results or conclusions?
Strengths (bullet list)
At least 3 bullets such as:
"Clear explanation of the dataset and labelling process."
"Nice use of examples in the Results section."
"The motivation for helping learners is very compelling."
Suggestions for Improvement
At least 3 bullets, each with a specific, actionable suggestion:
"Consider adding a small table that directly compares Prompt A vs. Prompt B accuracy."
"The architecture diagram is good, but you might label the boxes more clearly."
"The ethical considerations section could briefly mention bias or potential misuse."
Questions / Clarifications
2–3 questions that might help them think deeper:
"Did you notice any difference in performance for shorter vs. longer inputs?"
"If you had more time, which part of the pipeline would you improve first?"
"How sensitive were the results to your choice of temperature / number of shots?"
Overall Impression (1–2 sentences)
A short closing reflection:
"Overall, this is a solid project with clear motivation and interesting results. With a bit more clarity in the evaluation section, it would be even stronger."
5. Tone & Professionalism

Please:
Assume your classmates worked hard and did their best.
Write as if you’re a collaborator, not a judge.
Avoid sarcasm, dismissive comments, or personal remarks.
If you’re unsure how something works, ask a curious question instead of assuming it’s wrong.
Examples:
"I wasn’t fully sure how you created your validation split—could you clarify that?"
"I wonder if using more examples in the prompt would change your results; have you tried that?"
6. Why This Matters

Giving and receiving feedback is a key part of doing work in machine learning, data science, and industry in general. Good peer reviews:
Help the authors see their project from a fresh perspective
Help the reviewer learn to read and critique ML/LLM work
Make the overall quality of the projects better
Take it seriously, but don’t stress—just aim to be clear, kind, honest, and specific.
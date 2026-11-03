# P4 Presentation Requirements

## General Requirements

- All team members must participate in the presentation.
- Presentations should be approximately 15 minutes in length.
- Focus on demonstrating the product from a user and stakeholder perspective.
- Do **not** perform a code walkthrough unless specifically requested.

---

# Presentation Agenda

## 1. Introduction (5-6 Minutes)

### Team Introduction
Briefly introduce:
- Team name
- Team members
- Individual contributions or areas of ownership

### Product Introduction
Provide a high-level overview of your application.

At a minimum, explain:
- The theme of the application, and the theme, format, and quantity of data used.
- What need/demographic it addresses (conversational chatbot with RAG capabilites... but for who?)
- What RAG is, what an LLM is, and the different AI models used in your application.
- What a VectorDB is, your embedding strategy, and how Vector embeddings benefit your RAG workflows (semantic search!)
- The front end framework or library you used, and why.

### Presentation Overview
Briefly explain what the audience will see:
- Product demonstration
- Discussion of project outcomes
- Team retrospective

---

## 2. Product Walkthrough (7-8 Minutes)

Treat this section like a stakeholder demo. Show the functionality your team delivered and explain how it satisfies the project requirements. Feel free to find ways to fill time while your LLM thinks, or have a couple generated responses on the webpage already (on separate tabs?). But make sure to show it running a few times at least. Maybe prioritize the quickest requests?


### The Dashboard

Demonstrate:
- The general layout and features in your dashboard. Did you do anything cool besides a chat box?

Discuss:
- The layout of the UI, and how it promotes a seamless, intuitive user experience.
- Make sure to call out any specifics that your front end framework/library of choice allowed for!


---

### General Chat

Demonstrate:
- At least one successful conversational query, with an appropriate response. 
- At least one query that is refused, or otherwise not answered. Something your chatbot WON'T do.

Discuss:
- Your prompt engineering strategy, and how it comes across in the LLM's responses.
- How the persona given to your LLM benefits the user experience or fits the theme of the application.
- How you set the guardrails to prevent certain queries from being answered.

---

### Data Ingestion

Demonstrate:
- Ingesting data, either from the front end or through Swagger UI
- The data you ingest is your choice, but you must demonstrate the LLM's knowledge of that data

Discuss:
- The type of data you ingested, and how it's stored in the API

---

### RAG Chat

Demonstrate:
- At least one successful conversational query, with a response augmented by the data strored in your VectorDB. 
- At least one query that is refused, or otherwise not answered. Something your chatbot WON'T do.

Discuss:
- Your prompt engineering strategy, and how it comes across in the LLM's responses.
- How the persona given to your LLM benefits the user experience or fits the theme of the application.
- How you set the guardrails to prevent certain queries from being answered.

---


## 3. Mini Retrospective (3-5 Minutes)

As a team, reflect on the project experience.

### What Went Well

Examples:
- Strong team communication
- Effective Git workflow
- Clear division of responsibilities

---

### What Could Be Improved

Examples:
- Earlier decision making (models? front end strategy?)
- More frequent code reviews
- Better sprint planning

---

### If We Had Another Sprint

Use this time to explain how you've improve this iteration of the Project, given more time.

---

## Presentation Tips

### Focus on the User Experience
When demonstrating features, explain:
- What the user is doing
- What the system is doing (even if simulated)
- Why the feature is valuable

### Avoid Code Walkthroughs
Instead of discussing implementation details, demonstrate the completed functionality and business value. You may point out architectural choices, but keep the focus on the product.

### Share Participation
Ensure each team member presents at least one section of the product walkthrough and contributes to the retrospective discussion.

### Prepare your Speech
This is a product presentation, not an oral exam. Write down what you want to say as part of your presentation: this can help to keep your presentation in time and calm your nerves if you don't like public speaking.

### Prepare Visual Aids
A slide deck is not just nice to look at: it acts as a guide to help keep the presentation on track while helping the audience keep track of where you are in the presentation. Make sure not to read off your slides.

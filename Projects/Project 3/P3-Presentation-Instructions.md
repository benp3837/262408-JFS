# P3 Presentation Requirements

## General Requirements

- All team members must participate in the presentation.
- Presentations should be approximately 20 minutes in length.
- Focus on demonstrating the product from a user and stakeholder perspective.
- Do **not** perform a code walkthrough unless specifically requested by the instructor.

---

# Presentation Agenda

## 1. Introduction (2-3 Minutes)

### Team Introduction
Briefly introduce:
- Team name
- Team members
- Individual contributions or areas of ownership

### Product Introduction
Provide a high-level overview of your application.

At a minimum, explain:
- The Bank of CLI Full Stack App
- What business needs it addresses (moving a CLI banking tool to a Full Stack App with a Spring Boot Backend)
- Who the intended users are
- What "Full Stack" means and why it matters

### Presentation Overview
Briefly explain what the audience will see:
- Product demonstration
- Discussion of project outcomes
- Team retrospective

---

## 2. Product Walkthrough (12-15 Minutes)

Treat this section like a stakeholder demo. Show the functionality your team delivered and explain how it satisfies the project requirements. Also, since you already know what your next sprint will be and how it relates to the work of this current sprint, feel free to include callouts of how the work done this sprint prepares you for next sprint.

### Secure Access (Login & Registration)

Demonstrate:
- The registration flow for a new user
- The login flow for an existing user (And how JWTs fit into the process)
- Failed authentication attempt (invalid credentials / error state)

Discuss:
- How error states are handled 
- User-friendly feedback shown on failures

**Project Requirements Covered**
- Secure Access
- Gracefully handled error states

---

### The Dashboard

Demonstrate:
- Viewing the current account balance
- Viewing a list of recent transactions

Discuss:
- How the dashboard is the central hub for the user
- How balance and transactions are loaded (via your Service layer, not hardcoded in components)

**Project Requirements Covered**
- The Dashboard

---

### Deposit Transaction

Demonstrate:
- Depositing funds into an account
- The updated balance after deposit
- Client-side validation (e.g., rejecting empty fields or non-numeric input)

Discuss:
- How the form validates input before submission
- How the action is confirmed (toast / modal) and loading state shown

**Project Requirements Covered**
- Deposit
- Client-side validation
- Professional UX (feedback + loading states)

---

### Withdrawal Transaction

Demonstrate:
- A successful withdrawal
- An attempted withdrawal that is invalid (e.g., exceeds available funds, or negative value)
- The client-side validation catching the invalid input

Discuss:
- How invalid withdrawals are prevented on the client
- The error feedback shown to the user

**Project Requirements Covered**
- Withdraw
- Client-side validation
- Professional UX (feedback)

---

### Transfer Transaction

Demonstrate:
- Transferring funds between two accounts
- Updated balances for both accounts
- Reusable component usage (e.g., the same Button/Input used across deposit, withdraw, and transfer forms)

Discuss:
- How the transfer form reuses shared components
- How the UI simulates a safe, confirmable transfer

**Project Requirements Covered**
- Transfer
- Reusability
- Professional UX

---

### Handling API Responses in the Backend

Demonstrate:
- Where the data actually comes from ("Real" persistent database called to from a Spring Boot Backend)
- Loading states (spinner/skeleton) shown while waiting for a simulated response

Discuss:
- How the backend gathers data and responds to requests
- The Java Layered Architecture (Controller/Service/DAO)

---

### JWTs

Demonstrate:
- A brief look at how token-based auth with JWTs dictate what users can and can't do

Discuss:
- Why JWTs make for a more secure application
- How privileges are determined based on the JWT and its payload

**Project Requirement Covered**
- Authentication and Authorization

---

### Tests / Quality

Demonstrate:
- Run your tests (if you have any)
    - have a pre-made test report ready as a fall-back in case the live run goes wrong (screenshot is fine)
- if you do not have test then make sure to discuss what quality gates your team implemented to maintain a high level of confidence in the application
    - code reviews
    - pair programming
    - etc.

**Project Requirement Covered**
- Quality Standards

---

## 3. Mini Retrospective (3-5 Minutes)

As a team, reflect on the project experience.

### What Went Well

Examples:
- Strong team communication
- Effective Git workflow
- Clear division of responsibilities
- Successful component design / reusability

---

### What Could Be Improved

Examples:
- Earlier integration testing
- More frequent code reviews
- Better sprint planning
- More consistent styling across components

---

### If We Had Another Sprint

(Note that Project 4 is a completely different project, so this would only apply to this Sprint) Use this time to explain how you've improve this iteration of the Project, given more time.

---

## Presentation Tips

### Focus on the User Experience
When demonstrating features, explain:
- What the user is doing
- What the system is doing (even if simulated)
- Why the feature is valuable

### Avoid Code Walkthroughs
Instead of discussing implementation details, demonstrate the completed functionality and business value. You may point out architectural choices (like the Service layer), but keep the focus on the product.

### Share Participation
Ensure each team member presents at least one section of the product walkthrough and contributes to the retrospective discussion.

### Prepare your Speech
This is a product presentation, not an oral exam. Write down what you want to say as part of your presentation: this can help to keep your presentation in time and calm your nerves if you don't like public speaking.

### Prepare Visual Aids
A slide deck is not just nice to look at: it acts as a guide to help keep the presentation on track while helping the audience keep track of where you are in the presentation. Make sure not to read off your slides.

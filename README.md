# AI

<details><summary><span style="font-size:1.5em;">Overview</span></summary>

Don't forget `Ctrl + Shift + M` for preview window.

If you have any questions about how to make pretty, just ask.

The purpose of this document, is to be useful as a learning tool for creation,
and a revision tool later

Your task, is to go through what is already put in place, and add detail and description. I will be going through the lecture, and getting more topic from it to learn
And I will add examples to the descriptions you add.

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

<span style="color:aqua"> Aqua </span>

### TODO:
Swap new-lines with double-space


### Further Reading:

http://www.sci.brooklyn.cuny.edu/~sklar/teaching/s10/cis20.2/notes/lecIV.1-notes.pdf

</details>


---
## Lecture 1:
#### **What is AI?**

<details><summary><span style="font-size:1.25em;color:lime">The 4 categories:</span></summary>

 > **Acting Humanly**
 >
 > Acting like a person.
 >
 > Acting humanly places more emphasis on **the action, its outcome, and the product of the human thinking process.**
 >
 > > **Turing Test:**  
 > > Human interrogates entity via teletype for 5 mins. After, 5 mins, if the human cannot tell whether the entity was human or machine then entity can be counted as intelligent.
 >
 > > **Example:**  
 > > <span style="color:aqua"> AI-driven call-centre resembling humans for emphathetic service. </span>


 > **Thinking Humanly**
 >
 > Processing information similar ways as humans; thinking like a person.
 >
 > Thinking humanly is concerned with **modeling the human thinking process**.
 >
 > Two possible routes that humans use to find answer to a question:
 > - Reason about it to find the answer  
 > - Conduct experiments to find the answer
 >
 > > **Example:**  
 > > <span style="color:aqua"> Self-driving car trained on human decision making. </span>

 > **Thinking Rationally**
 >
 > Following Logic - Modelling thinking as a logical process, where conclusions are drawn based on some type of `symbolic logic`. **Focuses on how humans *should* think.**
 >
 > AI uses symbolic logic to capture the laws of rational thought as symbols that can be manipulated. Reasoning involves manipulating the symbols according to rules. The result is idealized model of human reasoning. This approach is more appealing to theorists - modeling how humans should think and reason in an ideal world.
 > > **Example:**  
 > > <span style="color:aqua"> Weather prediction system based on region history. </span>


 > **Acting Rationally**
 >
 > Decisions based around goal - performing actions that increase the value of the state of the agent or environment in which the agent is acting. An agent that is playing a game will act rationally if it tries to win the game. **Acting to achieve goals, given belief and understanding about the world.**
 >
 > When constructing an intelligent agent, the emphasis shifts from designing the theoretically best decision-making procedure to designing the best decision-making procedure possible within the circumstances in which the agent is acting.
 > > **Example:**  
 > > <span style="color:aqua"> Sat-Nav to find the fastest route between locations. </span>

</details>


<details><summary><span style="font-size:1.25em;color:lime">Rational Agents:</span></summary>


> **What is an AI System?**  
> An AI system is composed of a rational agent and its task environment.
>
> The agents act in the environment, which can contain other agents.

> **What is a Rational Agent?**  
> Entity which perceives and acts.
>
> It carries out an action with the best outcome after considering past and current perceptual input.
>
> Agents can be anything that perceives their environment, makes decisions, and acts upon the environment.

> **Task Environment:**  
> Problem the Agent is trying to solve.
>
>The environment is part of the real world or computational system that is inhabited by the agent. The agent obtains information about the environment in form of percepts (input that an intelligent agent is perceiving).
>
> **Properties:**
> - Fully or Partially Observable
>      - **(The level of information available to the agent.)**
> - Deterministic or Stochastic
>      - **(The extent of randomness.)**
> - Episodic or Sequential
>      - **(How actions taken effect future states of the world.)**
> - Static or Dynamic
>      - **(Activity of the environment during decision making.)**
> - Discrete or Continuous
>      - **(The amount of choices available to the agent.)**
> - Single- or Multi-Agent
>      - **(How many AIs are acting within the environment.)**

 </details>



---
## Lecture 2:
#### **How does Probabilistic AI work?**

<details><summary><span style="font-size:1.25em;color:lime">Intro to Probability:</span></summary>

<details><summary><span style="font-size:1.1em;color:aqua">Samples</span></summary>

> **Sample Space**  
> The collection of all possible outcomes and states of a system.  
> > **Example:**  
> > <span style="color:lime"> All potential states of a Dice Roll {1,2,3,4,5,6} </span>

> **Sample Point / Possible World / Atomic Event**  
> A single state of events in the world.
> > **Example (Dice Roll):**  
> > <span style="color:lime"> A roll with value (1) </span>

![alt text](https://www.mathsisfun.com/data/images/probability-sample-space.svg)

</details>

<details><summary><span style="font-size:1.1em;color:aqua">Single Events</span></summary>

> **Probabilistic Space / Probabilistic Model**  
> A sample space with a value.
> > **Example (Dice Roll):**  
> > <span style="color:lime"> P(1) = 1/6 </span>
![alt text](http://www.stat.yale.edu/Courses/1997-98/101/probeq.gif)

> **Event**  
> Any subset of Sample Points
> > **Example (Dice Roll):**  
> > <span style="color:lime"> P(x<4) = P(1) + P(2) + P(3) </span>

> **Complementray Event**  
> The inverse event, defined as all outcomes which do not contain X.
> > **Example (Dice Roll):**  
> > <span style="color:lime"> P(5') = 1 - ( P(1) + P(2) + P(3) + P(4) + P(6) ) </span>
>
![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7-o0L01HnvLNatPBBDKChhqHGYKzS4QNuuFcL0tsEndU9nVAm)

</details></details>


<details><summary><span style="font-size:1.25em;color:lime">Syntax for Propositions:</span></summary>

<details><summary><span style="font-size:1.1em;color:aqua">Syntax</span></summary>

> **Random Variables**  
> Any variable containing a sample space.  
> Always begins with a capital letter.
> > **Example (Dice Roll):**  
> > <span style="color:lime"> Die<sub>1</sub> = {1,...,6} </span>
>
>![alt text](https://www.mathsisfun.com/data/images/random-variable-1.svg)


> **Propositions:**  
> Set of sample points which equate to true.
> > **a:** `A(ω)=true`
> >
> > **¬a:** `A(ω)=false`
> >
> > **a ∧ b:** `A(ω)=true` & `B(ω)=true`
> >
> > **a ∨ b:** `(a ∧ b)` or `(¬a ∧ b)` or `(a ∧ ¬b)`

</details>

<details><summary><span style="font-size:1.1em;color:aqua">Variable Types</span></summary>

> **Boolean:**  
> Variable(condition) = true, also written as variable
> > **Example:**  
> > `Cavity(have?) = true`  
> > Proposition: `cavity` or `¬cavity`

> **Discrete:**  
> Variable contains an exhaustive and finite list of sample points.
> > **Example:**  
> > `Weather = {sun, rain, cloud, snow}`  
> > Proposition: `Weather = snow`

> **Continuous:**  
> Bounded or unbounded values.
> > **Example:**  
> > Proposition: `Temp = 12.5` or `Temp > 0.7`

</details>
</details>

<details><summary><span style="font-size:1.25em;color:lime">Types of Probability:</span></summary>

> **Prior (Unconditional) Probability**  
> Probability of sample point occurring.  
> > **Example:** `P(x=X) = 0.1`

> **Probability Distribution**  
> Probability of each possible sample point.  
> > **Example:** `P(Variable) = < 0.1, 0.4, 0.3, 0.2 >`

> **Joint Probability**  
> Probability of every atomic event in a set of variables.
>
> Every question about a domain can be answered by the joint distribution
because every event is a sum of sample points.  
> > **Example:**  
> > `P(Weather, Sun) = `
> >
> > | Weather=    | sun   | rain  | cloud | snow  |
> > | ------------|:-----:| -----:|:-----:| -----:|
> > | **Sun = true**  | 0.114 | 0.02  | 0.016 | 0.02  |
> > | **Sun = false** | 0.576 | 0.08  | 0.064 | 0.08  |

**Conditional (Posterior) Probability**
> **What does it mean?**  
> `P(b|a) = x`  
> Given a is all I know: `P(b) = x`
>
>```
               p(b)┌───
     p(a)┌─────────┤
         │    p(¬b)└───
    ─────┤
         │     p(b)┌───
    p(¬a)└─────────┤
              p(¬b)└───
```
>
> Notation for conditional distributions:  
> `p(B|a) = < p(b|a), p(¬b|a) >`  
>
> New evidence may be irrelevant:  
> `p(b|a,C) = p(b|a) = x`  


> **Rearrangement:**
> ```
         p(a∧b)
p(a|b) = ──────  if p(b)!=0
          p(b)
```
> [JAMES]

> **Product Rule:**  
> `P(a∧b) =P(a|b)P(b) =P(b|a)P(a)`
> [JAMES]


> **Chain Rule:**  
> Just a long version of the product rule...
> [JAMES]


> **Bayes Rule:**  
> `p(A|B) = p(B|A)*p(A)/P(B)`
> [JAMES]

**Marginal Probability:**
> magic...
https://www.khanacademy.org/math/ap-statistics/analyzing-categorical-ap/distributions-two-way-tables/v/marginal-distribution-and-conditional-distribution
> P(X) [add up column]
> [JAMES]

**Inference by Enumeration:**
> **Enumeration Table**  
>
>> [JAMES]
>
> **Normalization**  
>
>> [JAMES]

</details>

---
#### Lecture 3:
Talkative Pepper
> Uses multiple machine learning models to train


Baysean probability
>Event E occurs, with a series of Sub-events S
by defining the probability of each s, we can define the probability of E being caused by an unknown C



Number of Parameters (probabilities) within a system of N binary variables, in a setup where k nodes act as parents, is equal to N*2<sup>k</sup>
















---
#Algorithms:
Inference by Enumeraiton
Infererence




---
#Markov Models:
http://www.cs.columbia.edu/~mcollins/cs4705-spring2019/



---
#Assessment:

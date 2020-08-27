# Take Two API

### Emb(race): Diverse Representation

Technology has the power to drive action. And right now, a call to action is needed to eradicate racism. **Black lives matter.**

We recognize technology alone cannot fix hundreds of years of racial injustice and inequality, but when we put it in the hands of the Black community and their supporters, technology can begin to bridge a gap. To start a dialogue. To identify areas where technology can help pave a road to progress.

This project is an effort to utilize technology to analyze, inform, and develop policy to reform the workplace, products, public safety, and legislation.

This is one of three open source projects underway as part of the [Call for Code Emb(race) Spot Challenge](https://github.com/topics/embrace-call-for-code) led by contributors from IBM and Red Hat.

</br>

### Problem Statement

*Bias is learned and perpetuated in different ways (e.g. societal beliefs, misrepresentation, ignorance) that consequently create inequitable outcomes across all spheres of life.*

</br>

### Description of the Take Two Project

This solution provides a quick and simple tool for **content creators** to eliminate racial bias (both overt and subtle) from their content. 

This is underpinned by a crowd-sourced database of words and phrases that are deemed racially biased. These phrases are categorized in order to train an AI model on the significance of the context in which the language was used. Contributors to the project can be part of the crowdsourcing process by installing a browser extension. This API repo is part of the data capture process, which is used for modelling. 

There are a number of other repositories related to this project:

- [Take Two Data Science](https://github.com/embrace-call-for-code/taketwo-datascience) - Contains data science work for building and training the model.
- [Take Two Marker Chrome Extenstion](https://github.com/embrace-call-for-code/taketwo-marker-chromeextension) - Code for the Chrome extension used to crowdsource data for training the ML model. 


</br>

### Take Two Architecture

This API (highlighted in the following diagram) is part of the Call For Code Take Two MVP 1 delivery. This API is used to capture the data highlighted by users through the Take 2 Chrome extension tool.

![](images/architecture-highlighted.png)

</br>

### Description of Take Two API

This API is part of the Call For Code Take Two project. This API is used to capture the data crowdsourced by our contributors through the [Take 2 Chrome extension tool](https://github.com/embrace-call-for-code/taketwo-marker-chromeextension).

The API is used to fetch the defined categories of racial bias and serve them in the extension tool. It also captures the data highlighted by contributors and posts it to a backend database. This data is used to train an [ML model](https://github.com/embrace-call-for-code/taketwo-datascience) that can detect racial bias. 

</br>


### Authors

- User Researcher: Anna Rodriguez
- Designers: Naagma Timakondu, Sbusiso Mkhombe
- Tester: Merlina Escorcia
- Generalist: Ashley West, Jashu Gorsia, Yolanda Rabun
- Data Scientists: Naoki Abe, Alayt Issak
- Lead Developer: Johanna Saladas
- Architect: Steve Uniack
- Offering Manager: Iain  McCombe

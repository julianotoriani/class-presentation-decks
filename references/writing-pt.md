# Wording: patterns that were rejected, with the real rewrites

All examples come from one seminar deck. Its running example was a hospital sending lab reports ("laudos") to a lab, and the topics were RSA, quantum computers and lattice cryptography. "Before" is what was generated. "After" is what the group picked from the 2–3 options offered. Sometimes the group chose an option other than the recommended one; that's why you offer options and don't decide.

Sweep for one pattern at a time across the slides, the speech and the Q&A, then present the hits in batches.

## Contents
1. Contrast frames ("não é X, é Y")
2. Rhetorical questions answered right away
3. Teasers, reveals and callbacks
4. Punchlines, drama and fragments
5. Cleft sentences
6. Lead-ins and fillers
7. Aphorisms, myths and repeated disclaimers
8. Pronouns for things
9. Odd words and invented names
10. Sentences that leave the listener guessing
11. How to present the choices

## 1. Contrast frames ("não é X, é Y")

These are the most frequent. The fix is to say the positive statement directly. If the negated thing matters, give it its own plain sentence.

| before | after |
|---|---|
| Na prática não é tinta: é uma conta com curvas elípticas que é fácil de fazer e muito difícil de desfazer. | Na conexão de verdade, a mistura é uma conta com curvas elípticas: fácil de fazer e muito difícil de desfazer. |
| O programa não dá um resultado: dá uma chance para cada um. | O programa calcula uma chance para cada um. |
| O que quebra o RSA é outro algoritmo, o de Shor, que não faz busca. | O RSA é quebrado pelo algoritmo de Shor, que vem a seguir. |
| O algoritmo de Shor (1994) é outra coisa: aproveita um padrão que se repete… | O algoritmo de Shor (1994) aproveita um padrão que se repete… |
| O reticulado não cifra o laudo. Ele faz a etapa 1, combinar a chave… | O reticulado substitui as curvas elípticas na etapa 1, combinar a chave. As outras etapas continuam como hoje. |
| Testar todas as combinações não é o único caminho. O atacante também pode tentar… | Outro caminho para o atacante é transformar os vetores longos em curtos. |
| …não basta saber qual algoritmo está configurado. Tem que saber qual biblioteca e qual versão estão rodando. | …além do algoritmo configurado, a auditoria precisa saber qual biblioteca e qual versão estão rodando. |

The same family in English: "It's not X, it's Y", "This isn't about X. It's about Y", "X isn't enough; you need Y".

## 2. Rhetorical questions answered right away

The group rewrote all seven of these, including the ones that only repeated the slide title. Start with the answer.

| before | after |
|---|---|
| Quanto isso ajuda? O número de rodadas é mais ou menos a raiz quadrada… | O número de rodadas é mais ou menos a raiz quadrada… |
| Quando? Ninguém sabe. Em 2019, … | Em 2019, … (opener cut) |
| E quem interceptou o X? Ele só tem a chave pública… | Quem interceptou o X só tem a chave pública… |
| Por que o mesmo ruído cresce? Medir em A e B é… | O mesmo ruído cresce porque medir em A e B é… |
| Por que a chave pública erra? Os pontos são os mesmos… | Os pontos são os mesmos… (answer first) |
| Lembram do Grover? Ele tira a raiz quadrada… | O Grover tira a raiz quadrada… |
| Como dá para combinar uma chave secreta falando em público? A explicação clássica é com tinta. | A explicação clássica de como combinar uma chave secreta falando em público é com tinta. |

## 3. Teasers, reveals and callbacks

| before | after |
|---|---|
| E aqui está o motivo de falar disso agora. | Isso já importa hoje por causa de um ataque simples. |
| Agora o truque. Esses dois vetores laranja… | Esses dois vetores laranja… |
| O detalhe importante é o tempo. Pela Lei 13.787… Guardem esse número, porque ele volta no final. | Pela Lei 13.787… (opener and callback both cut) |

## 4. Punchlines, drama and fragments

| before | after |
|---|---|
| Para o laudo, o ataque já começou. | (on screen) A gravação pode estar acontecendo hoje, mesmo sem computador quântico |
| E o NIST já marcou o fim: RSA e curvas elípticas ficam obsoletos depois de 2030… | Pelo calendário do NIST, RSA e curvas elípticas ficam obsoletos depois de 2030… |
| Esse é o problema que protege tudo: achar o ponto da grade mais perto de um lugar. | Achar o ponto da grade mais perto de um lugar é o problema difícil do reticulado. |
| O truque só funciona com muitas dimensões. | A segurança vem de usar muitas dimensões. |
| Para a maioria dos problemas não se conhece um jeito rápido de fazer isso. Para alguns, conhece. | Para a maioria dos problemas não se conhece um jeito rápido de fazer isso, só para alguns. |
| Mas usar o algoritmo certo não resolve tudo. | Só que a implementação também pode falhar. |

## 5. Cleft sentences

| before | after |
|---|---|
| O que o hospital diminuiu foi o tempo de migração. | O hospital diminuiu o tempo de migração. |
| O que o hospital conseguiu diminuir foi o tempo de migração, e a auditoria é o que comprova isso. | O hospital diminuiu o tempo de migração, e a auditoria comprova isso. |

## 6. Lead-ins and fillers

| before | after |
|---|---|
| Um detalhe: se rodar demais, a chance volta a cair. | Se rodar demais, a chance volta a cair. |
| Tem mais um detalhe: o pós-quântico só existe na versão mais nova… | Além disso, o pós-quântico só existe na versão mais nova… |
| É exatamente essa parte que o computador quântico ameaça. | É essa parte que o computador quântico ameaça. |
| …mas a barra caiu 20 vezes em seis anos. | …mas o número de qubits caiu 20 vezes em seis anos. (same words as the screen) |

## 7. Aphorisms, myths and repeated disclaimers

- An aphorism on screen, "A configuração pode dizer uma coisa e a conexão fazer outra.", became "O algoritmo usado pode ser diferente do configurado."
- An opener set up a myth only to knock it down ("a explicação mais comum engana… Se fosse assim… e não é."). It was cut from the speech; the myth's answer lives in the Q&A.
- A Q&A answer opened with "Não do jeito que costuma ser dito." and became "Não exatamente."
- "A ideia é a mesma" appeared 5 times. It was kept only where the simplified drawing starts and where it ends.

## 8. Pronouns for things

The rule is "ele/ela" only for people. For an algorithm, a number, a machine, a key, a company or an institution, repeat the noun or restructure.

| before | after |
|---|---|
| Sem ela, quem interceptar só vê bytes sem sentido. (ela = a criptografia) | Sem a chave, quem interceptar só vê bytes sem sentido. |
| …os dois números que multiplicados dão ele. | Até hoje ninguém conseguiu fatorar esse número. |
| …vale entender o que ele faz. (ele = computador quântico) | …vale entender o que um computador quântico faz. |
| A cada rodada, ele usa a conferência… (ele = Grover) | A cada rodada, o Grover usa a conferência… |
| O AES não, porque contra ele só existe o Grover. | O AES não, porque contra o AES só existe o Grover. |
| Por isso o hospital soma um ruído. Ele gera um deslocamento… | Por isso o hospital soma ao ponto um deslocamento pequeno e aleatório… |
| …precisa descobrir de qual ponto ele saiu. | …precisa descobrir de qual ponto o X saiu. |
| …então o arredondamento apaga ele. | …então o arredondamento apaga o ruído. |
| …tráfego de navegadores que passa por ela… (ela = Cloudflare) | …tráfego de navegadores que passa pela Cloudflare… |
| O código de referência dele, que muita gente copiou… (dele = Kyber) | O código de referência do Kyber, que muita gente copiou… |

## 9. Odd words and invented names

| before | after | why |
|---|---|---|
| O hospital sorteia uma chave secreta. | O hospital gera uma chave secreta aleatória. | "sortear" sounds like a raffle |
| ruído sorteado | ruído aleatório | same sweep |
| Na leitura, sai um só, sorteado por essas chances. | Na leitura, sai um resultado aleatório, seguindo essas chances. | same sweep |
| casinha (about 25 occurrences) | célula | the field's own term ("célula fundamental") |
| setas | vetores | the audience already knows the word |

## 10. Sentences that leave the listener guessing

| before | the question it raised | after |
|---|---|---|
| Uma delas chega no ponto do exemplo num passo só. | "What's the implication?" | O vetor B é 3 × vetor 1 + 2 × vetor 2: cai no ponto do exemplo. |
| Com duas setas curtas dá para chegar em qualquer ponto da grade. | "Is the grid based on the vectors, or the vectors on the grid?" | Somando os vetores um número inteiro de vezes, para frente ou para trás, chega-se em vários pontos. Todos esses pontos juntos são a grade, o reticulado. |

## 11. How to present the choices

One question per sentence or per group of related sentences. Each option shows the full new text, and says what happens to the speech when the screen changes.

```
Q: Slide 8, small line on screen: "O que quebra o RSA é outro algoritmo, o de Shor, que não faz busca."
   Speech ends: "O RSA é outra história, porque ele não cai por busca." Which replaces them?
   - cai por outro (Recommended): Slide: "O RSA cai por outro algoritmo, o de Shor." Speech: "Já o RSA cai por outro algoritmo, o de Shor."
   - vem a seguir: Slide: "O RSA é quebrado pelo algoritmo de Shor, que vem a seguir." Speech: "Já o RSA é quebrado por outro algoritmo, o de Shor, que vem a seguir."
   - speech only: Slide keeps only "Para o AES, basta usar chave de 256 bits." Speech: "Já o RSA cai pelo algoritmo de Shor."
```

The group picked "vem a seguir", not the recommendation. Apply exactly what they pick.

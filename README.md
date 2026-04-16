# Análise de Imagens com IA e OCR

Este projeto consiste em uma aplicação baseada em múltiplos serviços utilizando Docker, com um frontend em Gradio e dois backends desenvolvidos em FastAPI.

## Funcionalidades

- Upload de imagens pela interface web
- Geração automática de descrição da imagem com IA
- Extração de texto da imagem utilizando OCR
- Armazenamento da imagem e dos dados em banco SQLite

## Inteligência Artificial

O sistema utiliza o modelo:

- Salesforce/blip-image-captioning-base

Esse modelo é responsável por gerar descrições automáticas das imagens (image captioning).
A sáida do modelo se encontra em Inglês, com isso é usado também o deep_translator para a tradução ao Português.

## Arquitetura

A aplicação é dividida em três serviços:

- **gradio-visao** → Interface do usuário
- **api-visao** → Processamento da imagem (IA + OCR)
- **api-armazenamento** → Persistência de dados (SQLite + volume Docker)

Os serviços se comunicam por meio de APIs REST.
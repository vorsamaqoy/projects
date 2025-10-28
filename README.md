# Paddle Game con NEAT

Un semplice gioco paddle implementato in Python che utilizza l'algoritmo NEAT (NeuroEvolution of Augmenting Topologies) per addestrare una rete neurale a giocare autonomamente.

## Descrizione

Questo progetto dimostra come una rete neurale può imparare a giocare a un gioco paddle attraverso l'evoluzione genetica. Il gioco consiste in un paddle che deve colpire una palla che rimbalza per evitare che esca dal lato sinistro dello schermo.

## Caratteristiche

- Addestramento automatico tramite algoritmo NEAT
- Visualizzazione in tempo reale del processo di apprendimento
- Salvataggio del modello migliore
- Modalità test per vedere il modello addestrato in azione
- Visualizzazione delle statistiche (generazione, punteggio, fitness)

## Requisiti

Il progetto richiede le seguenti dipendenze:

```
neat-python
pygame
```

## Installazione

1. Clona o scarica questa repository
2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Assicurati di avere il file di configurazione `config-feedforward.txt` nella directory principale

## Utilizzo

### Addestrare il modello

Per avviare l'addestramento della rete neurale:

```bash
python train.py
```

L'addestramento:
- Visualizza il gioco in tempo reale per ogni genoma
- Mostra generazione corrente, punteggio e fitness migliore
- Si interrompe automaticamente quando un genoma raggiunge un punteggio di 20
- Salva il modello migliore in `best_genome.pkl`
- Può essere interrotto manualmente premendo ESC

### Testare il modello addestrato

Per vedere il modello addestrato in azione:

```bash
python test.py
```

Il test:
- Carica il modello salvato da `best_genome.pkl`
- Mostra il gioco con il paddle controllato dalla rete neurale
- Visualizza il punteggio raggiunto
- Può essere interrotto premendo ESC

## Come funziona

### Input della rete neurale

La rete neurale riceve 3 input:
- Posizione Y del paddle
- Posizione Y della palla
- Distanza verticale assoluta tra paddle e palla

### Output della rete neurale

La rete produce un singolo output:
- Valore > 0.5: muove il paddle verso il basso
- Valore ≤ 0.5: muove il paddle verso l'alto

### Sistema di fitness

- Il fitness aumenta di 1 punto ogni volta che il paddle colpisce la palla
- Penalità applicata se il paddle rimane fermo per più di 5 secondi
- Il gioco termina quando la palla tocca il lato sinistro dello schermo

### Parametri del gioco

- Dimensione schermo: 800x600 pixel
- Dimensione paddle: 8x80 pixel
- Velocità paddle: 10 pixel/frame
- Dimensione palla: 15x15 pixel
- Velocità palla: 10 pixel/frame (X e Y)
- Frame rate: 240 FPS

## File generati

- `best_genome.pkl`: Il genoma della rete neurale con le migliori prestazioni

## Note

- L'addestramento può richiedere diverse generazioni prima di ottenere risultati soddisfacenti
- Il modello si considera addestrato quando raggiunge un punteggio di 20
- L'alta velocità di frame (240 FPS) accelera il processo di addestramento

## Personalizzazione

Puoi modificare i seguenti parametri nei file:
- Dimensioni dello schermo e degli oggetti
- Velocità di movimento
- Soglia di punteggio per considerare l'addestramento completato
- Numero massimo di generazioni
- Input forniti alla rete neurale

## Licenza

Progetto open source - sentiti libero di modificarlo e migliorarlo!

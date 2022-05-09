# Otimização de Saque no Voleibol por meio de Particle Swarm Optimization
Foi criado um simulador de bola de voleibol com pygame, onde temos uma quadra de vôlei e uma bola que inicia numa posição x, y, z e que tem velocidades e rotação nesses 3 eixos principais

Com o método de enxame de partículas, iniciamos 100 partículas com parâmetros aleatórios, e por meio de aprendizado por reforço queremos que as partículas atinjam o melhor saque possível.

Existem 3 possíveis melhores saques: Maior velocidade final; Menor tempo até a bola encontrar o chão; Maior distância aos jogadores adversários.
Ajustando a função fitness desses 3 modos obteve-se 3 tipos de saques diferentes, mais conhecidos como Saque viagem, Saque flutuante e Saque jornada nas estrelas.

from pymm import Metamap
mm = Metamap('/home/feng/public_mm/bin/metamap')
mmos = mm.parse(['John had a huge heart attack and fever.'])

for idx, mmo in enumerate(mmos):
    for jdx, concept in enumerate(mmo):
        if concept.ismapping == 0 or 1:
            print(concept.cui, concept.score, concept.matched,
                  concept.matchedstart, concept.matchedend)
            print(concept.semtypes, concept.ismapping)

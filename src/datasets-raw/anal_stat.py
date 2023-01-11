
import spacy

from utils.rouge_score import evaluate_rouge

nlp = spacy.load("en_core_sci_md", disable=['tagger', 'ner'])

def tokenize_sent(text_src):
    doc_src = nlp(text_src)
    doc_src = list(doc_src.sents)
    out_sents = []
    for sent in doc_src:
        out_sents.append(sent.text)
    return out_sents

intro_text = "The objective of the work presented here is to study the mechanism of radiative line driving and the corresponding properties of the winds of possible generations of very massive stars at extremely low metallicities and to investigate the principal influence of these winds on ionizing fluxes and observable ultraviolet spectra. The basic new element of this approach, needed in the domain of extremely low metallicity, is the introduction of depth dependent force multipliers representing the radiative line acceleration. To calculate our wind models we take into account the improvements accomplished during the last decade with regard to atomic physics and line lists (see @xcite, @xcite). Because of the depth dependent force multipliers a new formulation of the critical point equations is developed and a new iterative solution algorithm for the complete stellar wind problem is introduced (section 4)."

rest_text = "In this section we develop a fast algorithm to calculate stellar wind structures and mass - loss rates from the equation of motion (eq.[eom1 ]) using a radiative line acceleration parametrized in the form of eq.[fmp3 ]. After the new concept to calculate stellar wind structures with variable force multipliers has been introduced and tested by comparing with the observed wind properties of o - stars in the galaxy and the smc, we are now ready for an application on very massive stars. The purpose of this first study is to provide an estimate about the strengths of stellar winds at very low metallicity for very massive hot stars in a mass range roughly between 100 to 300 m@xmath3. The goal of this paper is to investigate systematically the role of winds as function of metallicity and stellar parameters for hot stars in a mass range between 100 to 300 m@xmath3. With our new approach to describe line driven stellar winds at extremely low metallicity we were able to make first predictions of stellar wind properties, ionizing fluxes and synthetic spectra of a possible population of very massive stars in this range of metallicity @xmath1. We have demonstrated that the normal scaling laws, which predict stellar - mass loss rates and wind momenta to decrease as a power law with @xmath1 break down at a certain threshold and we have replaced the power - law by a different fit - formula. We were able to disentangle the effects of line - blocking and line - blanketing on the ionizing fluxes and found that while the number of photons able to ionize hydrogen and neutral helium is barely affected by metallicity ( and stellar luminosity ), there is a significant increase of the photons which can ionize oii, neii, ciii, with decreasing metallicity, the effect being strongest for those ionic species with ionization edges closest to the heii absorption edge .[discussion and future work] the heii ionizing photons are very strongly affected by metallicity ( and luminosity ) through the strengths of stellar winds. We also calculated synthetic spectra and were able to present for the first time predictions of uv spectra of very massive stars at extremely low metallicities. We learned that the presence of stellar winds leads to observable broad spectral line features, which might be used for spectral diagnostics, should such an extreme stellar population be detected at high redshift. We find these first steps very encouraging to proceed with our calculations towards a number of improvements and extensions in the future. We also have to increase the range of effective temperatures, since the zero age main sequences of very massive stars are shifted beyond 60000k for metallicities as low as in this paper ( @xcite, @xcite, @xcite, @xcite ). In this way, we will be able to make improved predictions about the influence of stellar winds on the evolution of very massive stars and on the evolution of galaxies through deposition of matter, radiation, momentum and energy. However, it is very likely that an early generation of very massive stars will have an abundance pattern substantially different from the sun, in particular with regard to the ratio of @xmath5 to iron group elements."

intro_sents = tokenize_sent(intro_text)
rest_sents = tokenize_sent(rest_text)

for sent_num, isent in enumerate(intro_sents):
    most_similar_from_rest = []
    for s_num_det, sent in enumerate(rest_sents):
        most_similar_from_rest.append((sent, evaluate_rouge([sent], [isent])[1] + evaluate_rouge([sent], [isent])[2]))

    most_similar_from_rest = sorted(most_similar_from_rest, key=lambda x: x[1], reverse=True)
    s = 0
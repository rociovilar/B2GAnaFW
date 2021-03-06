header = """
### *****************************************************************************************
### Usage:
###    The globalTag is automatically chosen according to the input 'DataProcessing' value. 
###    However it can be explictily specified to override the default option.
###    Remember that the value of 'DataProcessing' is not set by default. The user has the choice of MC50ns, MC25ns, Data50ns, Data25ns. 
###
### Examples: 
###    Running on 25 ns MC:
###    cmsRun b2gedmntuples_cfg.py maxEvents=1000 DataProcessing='MC25ns'
###    Running on 25 ns data (Run2015 A, B, and C):
###    cmsRun b2gedmntuples_cfg.py maxEvents=1000 DataProcessing='Data25ns'
###    Running on 25 ns data (Run2015 D and MiniAODv2):
###    cmsRun b2gedmntuples_cfg.py maxEvents=1000 DataProcessing='Data25nsv2'
###    Running on 50 ns MC:
###    cmsRun b2gedmntuples_cfg.py maxEvents=1000 DataProcessing='MC50ns'
###    Running on 50 ns data:
###    cmsRun b2gedmntuples_cfg.py maxEvents=1000 DataProcessing='Data50ns'
###
### *****************************************************************************************
"""
print header

import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as opts
import copy

options = opts.VarParsing ('analysis')

options.register('sample',
                 '/store/mc/RunIISpring15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/00000/0014DC94-DC5C-E511-82FB-7845C4FC39F5.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')

options.register('outputLabel',
                 'B2GEDMNtuple.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Output label')

options.register('DataProcessing',
                 "",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Data processing types. Options are: MC50ns, MC25ns, Data50ns, Data25ns Data25nsv2')

options.register('lheLabel',
                 "",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'LHE module label, MC sample specific. Can be: externalLHEProducer')

### Expert options, do not change.
options.register('useNoHFMET',
                 True,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Adding met without HF and relative jets')

options.register('usePrivateSQLite',
                 True,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Take Corrections from private SQL file')

options.register('forceResiduals',
                 None,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Whether to force residuals to be applied')

options.register('globalTag',
                 '',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Global Tag')

options.register('wantSummary',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Want summary report')

### Events to process: 'maxEvents' is already registered by the framework
options.setDefault('maxEvents', 10)

options.parseArguments()
  
if options.DataProcessing == "":
  sys.exit("!!!!Error: Enter 'DataProcessing' period. Options are: 'MC50ns', 'MC25ns', 'Data50ns', 'Data25ns', 'Data25nsv2'.\n")

if options.globalTag != "": 
  print "!!!!Warning: You have chosen globalTag as", options.globalTag, ". Please check if this corresponds to your dataset."
else: 
  if options.DataProcessing=="MC50ns":
    options.globalTag="MCRUN2_74_V9A"
  elif options.DataProcessing=="MC25ns":
    options.globalTag="MCRUN2_74_V9"
  elif options.DataProcessing=="Data50ns":
    options.globalTag="74X_dataRun2_Prompt_v0"
  elif options.DataProcessing=="Data25ns":
    options.globalTag="74X_dataRun2_Prompt_v1"
  elif options.DataProcessing=="Data25nsv2":
    options.globalTag="74X_dataRun2_Prompt_v2"
  else:
    sys.exit("!!!!Error: Wrong DataProcessing option. Choose any of the following options for 'DataProcessing': 'MC50ns', 'MC25ns', 'Data50ns', 'Data25ns', 'Data25nsv2'\n") 

if "Data" in options.DataProcessing:
  print "!!!!Warning: You have chosen to run over data. lheLabel will be unset.\n"
  lheLabel = ""

###inputTag labels
rhoLabel          = "fixedGridRhoFastjetAll"
muLabel           = 'slimmedMuons'
elLabel           = 'slimmedElectrons'
jLabel            = 'slimmedJets'
jLabelNoHF        = 'slimmedJets'
jLabelAK8         = 'slimmedJetsAK8'

rhoLabel = 'fixedGridRhoFastjetAll'
pvLabel           = 'offlineSlimmedPrimaryVertices'
convLabel         = 'reducedEgamma:reducedConversions'
particleFlowLabel = 'packedPFCandidates'    
metLabel = 'slimmedMETs'
metNoHFLabel = 'slimmedMETsNoHF'

triggerResultsLabel = "TriggerResults"
triggerSummaryLabel = "hltTriggerSummaryAOD"
hltMuonFilterLabel       = "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f40QL3crIsoRhoFiltered0p15"
hltPathLabel             = "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"
hltElectronFilterLabel  = "hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8"
lheLabel = "externalLHEProducer"

### Including QGL: ensuring the database onject can be accessed
qgDatabaseVersion = 'v1' # check https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion

triggerResultsLabel    = "TriggerResults"
triggerSummaryLabel    = "hltTriggerSummaryAOD"
hltMuonFilterLabel     = "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f40QL3crIsoRhoFiltered0p15"
hltPathLabel           = "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"
hltElectronFilterLabel = "hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8"

print "\nRunning with DataProcessing option ", options.DataProcessing, " and with global tag", options.globalTag, "\n" 

process = cms.Process("b2gEDMNtuples")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.categories.append('HLTrigReport')
### Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(options.wantSummary) )
### Number of maximum events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
### Source file
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
        options.sample
        )
)
### Setting global tag 
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag.globaltag = options.globalTag 

### -------------------------------------------------------------------------------------------
###  QGL


from CondCore.DBCommon.CondDBSetup_cfi import *
QGPoolDBESSource = cms.ESSource("PoolDBESSource",
      CondDBSetup,
      toGet = cms.VPSet(),
      connect = cms.string('frontier://FrontierProd/CMS_COND_PAT_000'),
)

for type in ['AK4PFchs','AK4PFchs_antib']:
  QGPoolDBESSource.toGet.extend(cms.VPSet(cms.PSet(
    record = cms.string('QGLikelihoodRcd'),
    tag    = cms.string('QGLikelihoodObject_'+qgDatabaseVersion+'_'+type),
    label  = cms.untracked.string('QGL_'+type)
  )))

### -------------------------------------------------------------------------------------------



#process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("RecoEgamma/PhotonIdentification/PhotonIDValueMapProducer_cfi")
process.load("RecoEgamma.ElectronIdentification.ElectronIDValueMapProducer_cfi")
#process.load('RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV51_cff')

### External JECs =====================================================================================================

corrections = ['L1FastJet', 'L2Relative', 'L3Absolute']
if ("Data" in options.DataProcessing and options.forceResiduals):
  corrections.append['L2L3Residual']

if options.usePrivateSQLite:
    jLabel = 'updatedPatJetsAK4'
    jLabelAK8 = 'updatedPatJetsAK8'
    
    from CondCore.DBCommon.CondDBSetup_cfi import *
    import os
    if options.DataProcessing=="Data50ns":
      era="Summer15_50nsV5_DATA" 
    elif options.DataProcessing=="Data25ns":
      era="Summer15_25nsV2_DATA" 
    elif options.DataProcessing=="Data25nsv2":
      era="Summer15_25nsV2_DATA" 
    elif options.DataProcessing=="MC50ns":
      era="Summer15_50nsV5_DATA" 
    elif options.DataProcessing=="MC25ns":
      era="Summer15_25nsV2_MC" 
    dBFile = era+".db"
    print "\nUsing private SQLite file", dBFile, "\n"
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                               connect = cms.string( "sqlite_file:"+dBFile ),
                               toGet =  cms.VPSet(
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
                label= cms.untracked.string("AK4PF")
                ),
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),
                label= cms.untracked.string("AK4PFchs")
                ),
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK8PF"),
                label= cms.untracked.string("AK8PF")
                ),
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK8PFchs"),
                label= cms.untracked.string("AK8PFchs")
                ),
            )
                               )
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')
    
    process.load("PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff")
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated, patJetsUpdated
    process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
      rho = cms.InputTag("fixedGridRhoFastjetAll"),
      src = cms.InputTag("slimmedJets"),
      
      levels = corrections )
    process.updatedPatJetsAK4 = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
      )
    
    process.patJetAK8CorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJetsAK8"),
      rho = cms.InputTag("fixedGridRhoFastjetAll"),
      levels = corrections )

    process.updatedPatJetsAK8 = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJetsAK8"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetAK8CorrFactorsReapplyJEC"))
      )

jecUncertaintyFile="PhysicsTools/PatUtils/data/Summer15_50nsV4_DATA_UncertaintySources_AK4PFchs.txt"

### =====================================================================================================

#################################################
## After 7.4.0, only need to make AK8 gen jets.
## The rest are stored by default in MiniAOD directly. 
#################################################

## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", 
    src = cms.InputTag("packedGenParticles"), 
    cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16")
    )
## Fat GenJets
if "MC" in options.DataProcessing: 
    from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
    process.ak8GenJetsNoNu = ak4GenJets.clone(
        rParam = cms.double(0.8),
        src = cms.InputTag("packedGenParticlesForJetsNoNu")
    )

    ## SoftDrop fat GenJets (two jet collections are produced, fat jets and subjets)
    from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
    from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
    process.ak8GenJetsNoNuSoftDrop = ak4GenJets.clone(
        rParam = cms.double(0.8),
        src = cms.InputTag("packedGenParticlesForJetsNoNu"),
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.1),
        beta = cms.double(0.0),
        R0   = cms.double(0.8),
        useExplicitGhosts = cms.bool(True),
        writeCompound = cms.bool(True),
        jetCollInstanceName=cms.string("SubJets")    
    )

### ---------------------------------------------------------------------------
### Removing the HF from the MET computation as from 7 Aug 2015 recommendations
### ---------------------------------------------------------------------------
if options.useNoHFMET:
   process.noHFCands = cms.EDFilter("CandPtrSelector",
                                     src=cms.InputTag("packedPFCandidates"),
                                     cut=cms.string("abs(pdgId)!=1 && abs(pdgId)!=2 && abs(eta)<3.0")
                                     )

#jets are rebuilt from those candidates by the tools, no need to do anything else
### =================================================================================

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

#For a full met computation, remove the pfCandColl input
runMetCorAndUncFromMiniAOD(process,
                           isData=("Data" in options.DataProcessing),
                           )

if options.useNoHFMET:
    runMetCorAndUncFromMiniAOD(process,
                               isData=("Data" in options.DataProcessing),
                               pfCandColl=cms.InputTag("noHFCands"),
                               postfix="NoHF"
                               )
    jLabelNoHF = 'patJetsNoHF'

### -------------------------------------------------------------------
### the lines below remove the L2L3 residual corrections when processing data
### -------------------------------------------------------------------

if ("Data" in options.DataProcessing and  options.forceResiduals):
  #Take new pat jets as input of the entuples
  process.patJetCorrFactors.levels = corrections 
  if options.useNoHFMET:
    process.patJetCorrFactorsNoHF.levels = corrections 
else: 
    process.patPFMetT1T2Corr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT1T2SmearCorr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2Corr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2SmearCorr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.shiftedPatJetEnDown.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    process.shiftedPatJetEnUp.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    if options.useNoHFMET:
          process.patPFMetT1T2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
          process.patPFMetT1T2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
          process.patPFMetT2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
          process.patPFMetT2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
          process.shiftedPatJetEnDownNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
          process.shiftedPatJetEnUpNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
### ------------------------------------------------------------------

### ------------------------------------------------------------------
### Configure UserData
### ------------------------------------------------------------------
    
### Selected leptons and jets


process.skimmedPatMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag(muLabel),
    cut = cms.string("pt > 0.0 && abs(eta) < 2.4")
    )


process.skimmedPatPhotons = cms.EDFilter(
    "PATPhotonSelector",
    src = cms.InputTag("slimmedPhotons"),
    cut = cms.string("pt > 30 && abs(eta) < 2.4"),

)


process.skimmedPatElectrons = cms.EDFilter(
    "PATElectronSelector",
    src = cms.InputTag(elLabel),
    cut = cms.string("pt > 10 && abs(eta) < 2.5")
    )

process.skimmedPatMET = cms.EDFilter(
    "PATMETSelector",
    src = cms.InputTag(metLabel, "", "RECO"),
    cut = cms.string("")
    )

process.skimmedPatMETNoHF = cms.EDFilter(
    "PATMETSelector",
    src = cms.InputTag(metNoHFLabel, "", "RECO"),
    cut = cms.string("")
    )

process.skimmedPatJets = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag(jLabel),
    cut = cms.string(" pt > 25 && abs(eta) < 5.")
    )

process.skimmedPatJetsAK8 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag(jLabelAK8),
    cut = cms.string("pt > 100 && abs(eta) < 5.")    
    )


process.eventUserData = cms.EDProducer(
    'EventUserData',
    pileup = cms.InputTag("slimmedAddPileupInfo"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
)

process.muonUserData = cms.EDProducer(
    'MuonUserData',
    muonLabel = cms.InputTag("skimmedPatMuons"),
    pv        = cms.InputTag(pvLabel),
    packedPFCands = cms.InputTag("packedPFCandidates"),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltMuonFilter  = cms.InputTag(hltMuonFilterLabel),
    hltPath            = cms.string("HLT_IsoMu40_eta2p1_v11"),
    hlt2reco_deltaRmax = cms.double(0.1),
    # mainROOTFILEdir    = cms.string("../data/")
    )

process.jetUserData = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag(jLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2),
    )


process.jetUserDataNoHF = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag(jLabelNoHF),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2),
    )


process.jetUserDataAK8 = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag(jLabelAK8),
    pv        = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2)
)


process.electronUserData = cms.EDProducer(
    'ElectronUserData',
    eleLabel   = cms.InputTag("skimmedPatElectrons"),
    pv         = cms.InputTag(pvLabel),
    packedPFCands = cms.InputTag("packedPFCandidates"),
    conversion = cms.InputTag(convLabel),
    rho        = cms.InputTag(rhoLabel),
    triggerResults = cms.InputTag(triggerResultsLabel),
    triggerSummary = cms.InputTag(triggerSummaryLabel),
    hltElectronFilter  = cms.InputTag(hltElectronFilterLabel),  ##trigger matching code to be fixed!
    hltPath             = cms.string("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"),
    electronVetoIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto"),
    electronLooseIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose"),
    electronMediumIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium"),
    electronTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight"),
    electronHEEPIdMap = cms.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV60"), 
    eleMediumIdFullInfoMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium"),
    eleIdVerbose = cms.bool(True)
    )

process.photonUserData = cms.EDProducer(
    'PhotonUserData',
    rho                     = cms.InputTag(rhoLabel),
    pholabel                = cms.InputTag("slimmedPhotons"),
    phoLooseIdMap           = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-PHYS14-PU20bx25-V2-standalone-loose"),
    phoMediumIdMap          = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-PHYS14-PU20bx25-V2-standalone-medium"),
    phoTightIdMap           = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-PHYS14-PU20bx25-V2-standalone-tight"),
    phoChgIsoMap            = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
    phoPhoIsoMap            = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
    phoNeuIsoMap            = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
    effAreaChHadFile        = cms.FileInPath("RecoEgamma/PhotonIdentification/data/PHYS14/effAreaPhotons_cone03_pfChargedHadrons_V2.txt"),
    effAreaNeuHadFile       = cms.FileInPath("RecoEgamma/PhotonIdentification/data/PHYS14/effAreaPhotons_cone03_pfNeutralHadrons_V2.txt"),
    effAreaPhoFile          = cms.FileInPath("RecoEgamma/PhotonIdentification/data/PHYS14/effAreaPhotons_cone03_pfPhotons_V2.txt"),
    full5x5SigmaIEtaIEtaMap = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIEta")
  )

process.photonJets = cms.EDProducer(
    'PhotonJets',
    phoLabel = cms.InputTag("skimmedPatPhotons"),
    pv        = cms.InputTag(pvLabel),
    rho               = cms.InputTag(rhoLabel),
    packedPFCands = cms.InputTag("packedPFCandidates"),
    jetLabel  = cms.InputTag("slimmedJetsAK8"),
    ebReducedRecHitCollection = cms.InputTag("reducedEgamma:reducedEBRecHits"),
    eeReducedRecHitCollection = cms.InputTag("reducedEgamma:reducedEERecHits")

    )

process.vertexInfo = cms.EDProducer(
    'VertexInfo',
    src  = cms.InputTag(pvLabel),
    )


### -------------------------------------------------------------------------------------------
###  QGL

process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets  = cms.InputTag("jetUserData")    # Could be reco::PFJetCollection or pat::JetCollection (both AOD and miniAOD)
process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs')        # Other options: see https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion
process.QGTaggerNoHF = copy.deepcopy(process.QGTagger)
process.QGTaggerNoHF.srcJets  = cms.InputTag("jetUserDataNoHF")
### -------------------------------------------------------------------------------------------

process.jetUserDataQGL = cms.EDProducer(
  'QGLUserData',
  jetLabel = cms.InputTag("jetUserData"),
  qgtagger =  cms.InputTag("QGTagger", "qgLikelihood"),
)

process.jetUserDataNoHFQGL = cms.EDProducer(
  'QGLUserData',
  jetLabel = cms.InputTag("jetUserDataNoHF"),
  qgtagger =  cms.InputTag("QGTaggerNoHF", "qgLikelihood"),
)

#
# Set up photon ID (VID framework)
#

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate

#useAOD = False
#if useAOD == True :
dataFormat = DataFormat.MiniAOD
#else :
#    dataFormat = DataFormat.MiniAOD

switchOnVIDPhotonIdProducer(process, dataFormat)
switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_PHYS14_PU20bx25_V2_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

#

my_eid_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',
                  'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff']
for idmod in my_eid_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


process.egmGsfElectronIDs.physicsObjectSrc = 'skimmedPatElectrons'
        
from PhysicsTools.PatAlgos.tools.pfTools import *
## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag('offlineSlimmedPrimaryVertices'))

#################################################


from PhysicsTools.CandAlgos.EventShapeVars_cff import *
process.eventShapePFVars = pfEventShapeVars.clone()
process.eventShapePFVars.src = cms.InputTag(particleFlowLabel)

process.eventShapePFJetVars = pfEventShapeVars.clone()
process.eventShapePFJetVars.src = cms.InputTag("skimmedPatJets")

process.centrality = cms.EDProducer("CentralityUserData",
    src = cms.InputTag("skimmedPatJets")
    )                                    

process.TriggerUserData = cms.EDProducer(
    'TriggerUserData',
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    storePrescales = cms.untracked.bool(True), 
    hltProcName = cms.untracked.string("HLT"), 
    objects = cms.InputTag("selectedPatTrigger")
    )                                 

hltProcForMETUserData = "PAT"
if options.DataProcessing=="Data25nsv2":
  hltProcForMETUserData = "RECO"

process.METUserData = cms.EDProducer(
  'TriggerUserData',
  bits = cms.InputTag("TriggerResults","",hltProcForMETUserData),
  prescales = cms.InputTag("patTrigger"),
  storePrescales = cms.untracked.bool(False), 
  hltProcName = cms.untracked.string(hltProcForMETUserData), 
  objects = cms.InputTag("selectedPatTrigger")
  )

process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)

### Including ntuplizer 

process.load("Analysis.B2GAnaFW.b2gedmntuples_cff")
process.options.allowUnscheduled = cms.untracked.bool(True)

process.edmNtuplesOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('B2GEDMNtuple.root'),
    outputCommands = cms.untracked.vstring(
    "drop *",
    "keep *_muons_*_*",
    "keep *_vertexInfo_*_*",
    "keep *_electrons_*_*",
    "keep *_photons_*_*",
    "keep *_photonjets_*_*",
    "keep *_jetsAK4_*_*",
    "keep *_jetsAK8_*_*",
    "keep *_eventShape*_*_*",
    "keep *_*_*centrality*_*",
    "keep *_met_*_*",
    "keep *_metFull_*_*",
    "keep *_eventInfo_*_*",
    "keep *_subjetsAK8_*_*",
    "keep *_subjetsCmsTopTag*_*_*",
    "keep *_jetKeysAK4_*_*",
    "keep *_jetKeysAK8_*_*",
    "keep *_subjetKeysAK8_*_*",
    "keep *_subjetsCmsTopTagKeys_*_*",
    "keep *_electronKeys_*_*",   
    "keep *_muonKeys_*_*",
    "keep *_TriggerUserData*_trigger*_*",
    "keep *_METUserData*_trigger*_*",
    "keep *_fixedGridRhoFastjetAll_*_*",
    "keep *_eventUserData_*_*",
    "keep *_HBHENoiseFilterResultProducer_*_*",
    "keep *_eeBadScFilter_*_*"
    ),
    dropMetaData = cms.untracked.string('ALL'),
    )

### keep NoHF jets if needed:
if( options.useNoHFMET ):
  process.edmNtuplesOut.outputCommands+=('keep *_jetsAK4NoHF_*_*',)

### keep info from LHEProducts if they are stored in PatTuples
if(options.lheLabel != ""):
  process.LHEUserData = cms.EDProducer("LHEUserData",
  lheLabel = cms.InputTag(options.lheLabel)
  )
  #process.analysisPath+=process.LHEUserData
  process.edmNtuplesOut.outputCommands+=('keep *_*LHE*_*_*',)
  process.edmNtuplesOut.outputCommands+=('keep LHEEventProduct_*_*_*',)

if "MC" in options.DataProcessing: 
    process.edmNtuplesOut.outputCommands+=(
        'keep *_generator_*_*',
        "keep *_genPart_*_*",
        "keep *_genJetsAK8_*_*",
        "keep *_genJetsAK8SoftDrop_*_*"
        )

process.edmNtuplesOut.fileName=options.outputLabel

#process.edmNtuplesOut.SelectEvents = cms.untracked.PSet(
#    SelectEvents = cms.vstring('filterPath')
#    )

#process.analysisPath += process.photonIDValueMapProducer

#process.fullPath = cms.Schedule(
#     process.analysisPath
#    )

process.endPath = cms.EndPath(process.edmNtuplesOut)


open('B2GEntupleFileDump.py','w').write(process.dumpPython())

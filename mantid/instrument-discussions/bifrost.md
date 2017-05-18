- user mid 2023 (among first 8)
- hot comms 2022

a4 = tank rotation -> continuous scan
a3 = sample scan

stroboscopic measurements

S(Q,\omega) -> actually S(Q_1, Q_2, \omega) (absolutely essential from day 1 of hot commissioning)
  -> check what SofQw does in Mantid
time scale seconds to minutes

up to 5 GigaBins

## Monitors

- scans -> need time resolved monitors
- no single shot, monitors integrated over intervals of seconds-minutes
- details still open

## Non-straight beam path

- path component approx. should be fine
- current fudging also

- L1 might be wavelength dependent (will be simulated soon)!


- normalization for detectors and for analysis (actually combined)

## "Continuous angle multiple analsysis"

- not via choppers
- several different analysis in series -> different wavelength band
- might be analyzed separately (neither MatrixWorkspace nor MDWorkspace)


- for live mode, it might be sufficient to reduce data only from a single arc

## InstrumentView

- 5000 pixels -> no issue

## Sample alignment / Calibration

- Group all pixels (3 tubes, or just central) hit by same analyzer
- Plot I(\lambda, A3) -> sample alignment
- might be possible to do this offline, if done in short intervals (few minutes)

- white beam, close slits until bragg peak goes darker (reduce background), should be automatizable
  - using attenuation to reduce flux

- vanadium runs -> normalization file (monthly basis)


- detector safety system: bragg peak too strong -> detector will ramp down voltage -> disables detector
  - mask detectors
  - notify user in NICOS?


- worst case 1e6 counts/s, mostly 10x
  - might actually be 1e7 before calibration in early hot commissioning (might use attenuator)

- will look into what is needed as toolbox for alignment and calibration

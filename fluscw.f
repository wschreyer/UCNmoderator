*$ CREATE FLUSCW.FOR
*COPY FLUSCW
*                                                                      *
*=== fluscw ===========================================================*
*                                                                      *
      DOUBLE PRECISION FUNCTION FLUSCW ( IJ    , PLA   , TXX   , TYY   ,
     &                                   TZZ   , WEE   , XX    , YY    ,
     &                                   ZZ    , NREG  , IOLREG, LLO   ,
     &                                   NSURF )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1989-2005      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*     New version of Fluscw for FLUKA9x-FLUKA200x:                     *
*                                                                      *
*     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     *
*     !!! This is a completely dummy routine for Fluka9x/200x. !!!     *
*     !!! The  name has been kept the same as for older  Fluka !!!     *
*     !!! versions for back-compatibility, even though  Fluscw !!!     *
*     !!! is applied only to estimators which didn't exist be- !!!     *
*     !!! fore Fluka89.                                        !!!     *
*     !!! User  developed versions  can be used for  weighting !!!     *
*     !!! flux-like quantities at runtime                      !!!     *
*     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     *
*                                                                      *
*     Input variables:                                                 *
*                                                                      *
*           Ij = (generalized) particle code (Paprop numbering)        *
*          Pla = particle laboratory momentum (GeV/c) (if > 0),        *
*                or kinetic energy (GeV) (if <0 )                      *
*    Txx,yy,zz = particle direction cosines                            *
*          Wee = particle weight                                       *
*     Xx,Yy,Zz = position                                              *
*         Nreg = (new) region number                                   *
*       Iolreg = (old) region number                                   *
*          Llo = particle generation                                   *
*        Nsurf = transport flag (ignore!)                              *
*                                                                      *
*     Output variables:                                                *
*                                                                      *
*       Fluscw = factor the scored amount will be multiplied by        *
*       Lsczer = logical flag, if true no amount will be scored        *
*                regardless of Fluscw                                  *
*                                                                      *
*     Useful variables (common SCOHLP):                                *
*                                                                      *
*     Flux like binnings/estimators (Fluscw):                          *
*          ISCRNG = 1 --> Boundary crossing estimator                  *
*          ISCRNG = 2 --> Track  length     binning                    *
*          ISCRNG = 3 --> Track  length     estimator                  *
*          ISCRNG = 4 --> Collision density estimator                  *
*          ISCRNG = 5 --> Yield             estimator                  *
*          JSCRNG = # of the binning/estimator                         *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE '(SCOHLP)'
*
      LOGICAL LFIRST
      SAVE LFIRST
      DATA LFIRST /.TRUE./
      IF (LFIRST) THEN
         WRITE (LUNOUT,*) 'Called custom fluscw'
         LFIRST = .FALSE.
      ENDIF

      FLUSCW = ONEONE
      LSCZER = .FALSE.

      IF (Ij == 8 .AND. ISCRNG == 2) THEN
         IF (JSCRNG == 1)  THEN
            IF (-PLA < 80e-12) THEN
               ! exclude neutrons below 80meV
               LSCZER = .TRUE.
            ENDIF
         ELSE IF (JSCRNG == 2) THEN
            IF (-PLA > 80e-12 .OR. -PLA < 14.7e-12) THEN
               ! exclude neutrons above 80meV or below 14.7meV (23.5%-90% quantile of 300K range)
               LSCZER = .TRUE.
            ENDIF
         ELSE IF (JSCRNG == 3) THEN
            IF (-PLA < 2e-12 .OR. -PLA > 14.7e-12) THEN
               ! exclude neutrons above 14meV or below 2meV (10%-76.5% quantile of 80K range)
               LSCZER = .TRUE.
            ENDIF
         ELSE IF (JSCRNG == 4) THEN
            IF (-PLA > 2e-12) THEN
               ! exclude neutrons above 2meV (He-II conversion range)
               LSCZER = .TRUE.
            ENDIF

         ENDIF
      ENDIF

      RETURN
*=== End of function Fluscw ===========================================*
      END


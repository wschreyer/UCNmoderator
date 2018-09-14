*$ CREATE USIMBS.FOR
*COPY USIMBS
*
*=== Usimbs ===========================================================*
*
      SUBROUTINE USIMBS ( MREG, NEWREG, FIMP )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 2001-2008      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*                                                                      *
*     USer defined IMportance BiaSing:                                 *
*                                                                      *
*     Created on   02 july 2001    by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*     Last change on 30-oct-08     by    Alfredo Ferrari               *
*                                                                      *
*     Input variables:                                                 *
*                Mreg = region at the beginning of the step            *
*              Newreg = region at the end of the step                  *
*     (thru common TRACKR):                                            *
*              Jtrack = particle id. (Paprop numbering)                *
*              Etrack = particle total energy (GeV)                    *
*       X,Y,Ztrack(0) = position at the beginning of the step          *
*  X,Y,Ztrack(Ntrack) = position at the end of the step                *
*                                                                      *
*    Output variable:                                                  *
*                Fimp = importance ratio (new position/original one)   *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE '(TRACKR)'
*
      FIMP   = ONEONE

*      R1 = SQRT(Xtrack(0)**2+Ytrack(0)**2+Ztrack(0)**2)
*      R2 = SQRT(Xtrack(Ntrack)**2+Ytrack(Ntrack)**2+Ztrack(Ntrack)**2)
*      IF ( R1 .GT. 350 ) R1 = 350
*      IF ( R2 .GT. 350 ) R2 = 350
*      IF ( R1 .LT. 50 ) R1 = 50
*      IF ( R2 .LT. 50 ) R2 = 50
*      FIMP = EXP( (R2 - R1)/30. )

      Y1 = Ytrack(0)
      Y2 = Ytrack(Ntrack)
      IF ( Y1 .GT. -85. ) Y1 = -85.
      IF ( Y1 .LT. -190. ) Y1 = -190.
      IF ( Y2 .GT. -85. ) Y2 = -85.
      IF ( Y2 .LT. -190. ) Y2 = -190.
      FIMP = EXP( (Y1 - Y2)/10. )

      RETURN
*
*======================================================================*
*                                                                      *
*     Entry USIMST:                                                    *
*                                                                      *
*     Input variables:                                                 *
*                Mreg = region at the beginning of the step            *
*                Step = length of the particle next step               *
*                                                                      *
*    Output variable:                                                  *
*                Step = possibly reduced step suggested by the user    *
*                                                                      *
*======================================================================*
*
      ENTRY USIMST ( MREG, STEP )
*
      IF ( STEP .GT. ONEONE ) STEP = HLFHLF * STEP
      RETURN
*=== End of subroutine Usimbs =========================================*
      END


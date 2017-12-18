# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module BinsAndBob
 Provides routines for binning molecular information calculating averages etc.

 also provides routines for generating required information for BoB
 and deciding whether to save polymers for BoB output

"""
import numpy as np
import polybits

class BinsAndBob:

    def __init__(self, name, parent_dataset, ax):
        super().__init__(name, parent_dataset, ax)
        self.multi_wt = np.zeros((polybits.MAX_MWD_BINS))
        self.multi_avbr = np.zeros((polybits.MAX_MWD_BINS))
        self.multi_wmass = np.zeros((polybits.MAX_MWD_BINS))
        self.multi_avg = np.zeros((polybits.MAX_MWD_BINS))
        self.multi_lgmid = np.zeros((polybits.MAX_MWD_BINS))


    def molbin(self, n):
        """Call this procedure to calculate current averages
        and MWD for polymers made in distribution n"""
        # var i,i1,ibin:integer
        # wttot,m_w,m_n,brav,lgstep,lgmin,lgmax,cplen:double

        polybits.react_dist[n].nummwdbins = np.min((polybits.react_dist[n].nummwdbins, polybits.MAX_MWD_BINS))
        # first find largest and smallest polymer
        lgmax = 0.0
        lgmin = 1.0e80

        i = polybits.react_dist[n].first_poly
        while True:
            cplen = polybits.br_poly[i].tot_len
            lgmax = np.max((lgmax, cplen))
            lgmin = np.min((lgmin, cplen))
            i = polybits.br_poly[i].nextpoly
            if i == 0:
                break

        lgmax = np.log10((lgmax*1.01) * polybits.react_dist[n].monmass)
        lgmin = np.log10((lgmin/1.01) * polybits.react_dist[n].monmass)
        lgstep = (lgmax - lgmin)/polybits.react_dist[n].nummwdbins

        #initialise bins and other counters
        for ibin in range(polybits.react_dist[n].nummwdbins): #1 to polybits.react_dist[n].nummwdbins 
            polybits.react_dist[n].wt[ibin] = 0.0
            polybits.react_dist[n].avbr[ibin] = 0.0
            polybits.react_dist[n].avg[ibin] = 0.0
            polybits.react_dist[n].wmass[ibin] = 0.0

        wttot = 0.0
        m_w = 0.0
        m_n = 0.0
        brav = 0.0

        # the assumption here is that polymers have been created on a weight basis
        i = polybits.react_dist[n].first_poly
        while True:
            cplen = polybits.br_poly[i].tot_len * polybits.react_dist[n].monmass
            ibin = np.trunc((np.log10(cplen) - lgmin)/lgstep) + 1
            ibin = int(ibin)
            wttot += 1
            m_w = m_w + cplen
            m_n = m_n + 1.0/cplen
            brav = brav + polybits.br_poly[i].num_br / polybits.br_poly[i].tot_len
            if (ibin <= polybits.react_dist[n].nummwdbins) and (ibin > 0):
                polybits.react_dist[n].wt[ibin] = polybits.react_dist[n].wt[ibin] + 1.0
                polybits.react_dist[n].avbr[ibin] = polybits.react_dist[n].avbr[ibin] + polybits.br_poly[i].num_br
                polybits.react_dist[n].avg[ibin] = polybits.react_dist[n].avg[ibin] + polybits.br_poly[i].gfactor
                polybits.react_dist[n].wmass[ibin] = polybits.react_dist[n].wmass[ibin] + polybits.br_poly[i].tot_len
            i = polybits.br_poly[i].nextpoly
            if i == 0:
                break

        # finalise bin data - ready for plotting
        for ibin in range(polybits.react_dist[n].nummwdbins): # 1 to polybits.react_dist[n].nummwdbins
            polybits.react_dist[n].avbr[ibin] = polybits.react_dist[n].avbr[ibin] / (polybits.react_dist[n].wmass[ibin] + 1.0e-80) * 500.0
            polybits.react_dist[n].avg[ibin] = polybits.react_dist[n].avg[ibin] / (polybits.react_dist[n].wt[ibin] + 1.0e-80)
            polybits.react_dist[n].wt[ibin] = polybits.react_dist[n].wt[ibin] / lgstep / wttot
            polybits.react_dist[n].lgmid[ibin] = lgmin + ibin*lgstep - 0.5*lgstep

        polybits.react_dist[n].M_w = m_w/wttot
        polybits.react_dist[n].M_n = wttot/m_n
        polybits.react_dist[n].brav = brav/wttot * 500.0



    def multimolbin(self, reqbins, weights, inmix):
        """ 
        Call this procedure to calculate current averages
        and MWD for all polymers made in all distributions
        with weights contained in weights array, and whether "in the mix" contained
        in inmix array
        """
        # var i,i1,ibin,n:integer
        # wttot,m_w,m_n,brav,lgstep,lgmin,lgmax,cplen,wtpoly:double
        self.multi_nummwdbins = np.min((reqbins, self.MAX_MWD_BINS))

        # first find largest and smallest polymer
        lgmax = 0.0
        lgmin = 1.0e80

        for n in range(1, 11): #1 to 10
            if inmix[n - 1] and (weights[n - 1] > 0.0):
                i = polybits.react_dist[n].first_poly
                while True:
                    cplen = polybits.br_poly[i].tot_len * polybits.react_dist[n].monmass
                    lgmax = np.max((lgmax, cplen))
                    lgmin = np.min((lgmin, cplen))
                    i = polybits.br_poly[i].nextpoly
                    if i == 0:
                        break

        lgmax = np.log10(lgmax * 1.01)
        lgmin = np.log10(lgmin / 1.01)
        lgstep = (lgmax - lgmin)/self.multi_nummwdbins

        #initialise bins and other counters
        for ibin in range(self.multi_nummwdbins):
            self.multi_wt[ibin] = 0.0
            self.multi_avbr[ibin] = 0.0
            self.multi_avg[ibin] = 0.0
            self.multi_wmass[ibin] = 0.0

        wttot = 0.0
        m_w = 0.0
        m_n = 0.0
        brav = 0.0

        # the assumption here is that polymers have been created on a weight basis
        for n in range(1, 11): #1 to 10
            if inmix[n - 1] and (weights[n - 1] > 0.0):
                i = polybits.react_dist[n].first_poly
                wtpoly = weights[n-1] / polybits.react_dist[n].npoly
                while True:
                    cplen = polybits.br_poly[i].tot_len*polybits.react_dist[n].monmass
                    ibin = np.trunc((np.log10(cplen) - lgmin) / lgstep) + 1 
                    wttot = wttot + wtpoly
                    m_w = m_w + cplen * wtpoly
                    m_n = m_n + wtpoly / cplen
                    brav = brav + polybits.br_poly[i].num_br / polybits.br_poly[i].tot_len * wtpoly
                    if (ibin <= self.multi_nummwdbins) and (ibin > 0):
                        self.multi_wt[ibin] = self.multi_wt[ibin] + wtpoly
                        self.multi_avbr[ibin] = self.multi_avbr[ibin] + polybits.br_poly[i].num_br * wtpoly
                        self.multi_avg[ibin] = self.multi_avg[ibin] + polybits.br_poly[i].gfactor * wtpoly
                        self.multi_wmass[ibin] = self.multi_wmass[ibin] + polybits.br_poly[i].tot_len * wtpoly
                    i = polybits.br_poly[i].nextpoly
                    if i == 0:
                        break

        # finalise bin data - ready for plotting
        for ibin in range(self.multi_nummwdbins):
            self.multi_avbr[ibin] = self.multi_avbr[ibin] / (self.multi_wmass[ibin] + 1.0e-80) * 500.0
            self.multi_avg[ibin] = self.multi_avg[ibin] / (self.multi_wt[ibin] + 1.0e-80)
            self.multi_wt[ibin] = self.multi_wt[ibin] / lgstep / wttot
            self.multi_lgmid[ibin] = lgmin + ibin * lgstep - 0.5*lgstep

        self.multi_m_w = m_w/wttot
        self.multi_m_n = wttot/m_n
        self.multi_brav = brav/wttot * 500.0

    def bobinit(self, n):
        """Call this before making any polymers"""
        for i in range(polybits.react_dist[n].numbobbins):
            polybits.react_dist[n].numinbin[i] = 0
            polybits.react_dist[n].nsaved = 0

    def bobcount(self, m, n):
        """
        checks to see whether or not to save this polymer
        (polymer m, from polybits.react_dist n)
        """
        ibin = np.trunc((np.log10(polybits.br_poly[m].tot_len * polybits.react_dist[n].monmass) - polybits.react_dist[n].boblgmin) / (polybits.react_dist[n].boblgmax - polybits.react_dist[n].boblgmin) * polybits.react_dist[n].numbobbins) + 1
        ibin = np.min((np.max((1, ibin)), polybits.react_dist[n].numbobbins))
        ibin = int(ibin)
        polybits.react_dist[n].numinbin[ibin] = polybits.react_dist[n].numinbin[ibin] + 1
        if polybits.react_dist[n].numinbin[ibin] <= polybits.react_dist[n].bobbinmax:  #  check to see whether to "save" the polymer
            polybits.br_poly[m].saved = True
            polybits.br_poly[m].bin = ibin
            polybits.react_dist[n].nsaved = polybits.react_dist[n].nsaved + 1
        else:
            polybits.br_poly[m].saved = False
            polybits.br_poly[m].bin = 0
            polybits.return_poly_arms(m)


    def polyconfwrite(self, n, Fname):
        # var i,atally,numarms,anum :integer
        #     first,tL1, tL2, tR1, tR2, m1,mc, npoly: integer
        #     enrich,polywt,armwt,armz,N_e :double


        polybits.react_dist[n].N_e = polybits.react_dist[n].M_e / polybits.react_dist[n].monmass
        # opening lines
        fout = open(Fname, 'w')

        fout.write('reactpol')
        fout.write('{:12f}'.format(polybits.react_dist[n].N_e))
        fout.write(polybits.react_dist[n].nsaved)

        atally = 0

        # loop through polymers, writing output
        npoly = polybits.react_dist[n].npoly
        N_e = polybits.react_dist[n].N_e
        i = polybits.react_dist[n].first_poly
        while True:
            if polybits.br_poly[i].saved:
                if polybits.react_dist[n].numinbin[polybits.br_poly[i].bin] <= polybits.react_dist[n].bobbinmax:
                    enrich = 1.0
                else:
                    enrich = polybits.react_dist[n].numinbin[polybits.br_poly[i].bin] / polybits.react_dist[n].bobbinmax

                # polywt = enrich/npoly #not used

                if polybits.br_poly[i].num_br == 0: #it's a linear polymer
                    fout.write(2)
                    atally = atally + 2
                    first = polybits.br_poly[i].first_end
                    armwt = 0.5*polybits.arm_pool[first].arm_len / polybits.br_poly[i].tot_len / npoly * enrich
                    armz = 0.5*polybits.arm_pool[first].arm_len / N_e
                    fout.write('-1 -1 1 -1 {:12f} {:15f}'.format(armz, armwt))
                    fout.write('0 -1 -1 -1 {:12f} {:15f}'.format(armz, armwt))
                else: # it's a branched polymer
                    numarms = 2*polybits.br_poly[i].num_br + 1
                    fout.write(numarms)  #number of arms
                    atally = atally + numarms
                    first = polybits.br_poly[i].first_end

                    #renumber segments starting from zero
                    m1 = first
                    anum = 0
                    while True:
                        polybits.arm_pool[m1].armnum = anum
                        m1 = polybits.arm_pool[m1].down
                        anum = anum+1
                        if m1 == first:
                            break

                    # now do output - loop over arms
                    m1 = first
                    while True:
                        armwt = polybits.arm_pool[m1].arm_len / polybits.br_poly[i].tot_len / npoly*enrich
                        armz = polybits.arm_pool[m1].arm_len / N_e
                        if polybits.arm_pool[m1].L1 == 0:
                            tL1 = -1
                        else:
                            mc = np.abs(polybits.arm_pool[m1].L1)
                            tL1 = polybits.arm_pool[mc].armnum

                        if polybits.arm_pool[m1].L2 == 0:
                            tL2 = -1
                        else:
                            mc = np.abs(polybits.arm_pool[m1].L2)
                            tL2 = polybits.arm_pool[mc].armnum

                        if polybits.arm_pool[m1].R1 == 0:
                            tR1 = -1
                        else:
                            mc = np.abs(polybits.arm_pool[m1].R1)
                            tR1 = polybits.arm_pool[mc].armnum

                        if polybits.arm_pool[m1].R2 == 0:
                            tR2 = -1
                        else:
                            mc = np.abs(polybits.arm_pool[m1].R2)
                            tR2 = polybits.arm_pool[mc].armnum

                        fout.write(tL1, tL2, tR1, tR2, '{:12f} {:15f}'.format(armz, armwt))
                        m1 = polybits.arm_pool[m1].down

                        if m1 == first:  #end output loop over arms
                            break
                # end of if (it's a linear or branched polymer )


            #end of "if saved"
            i = polybits.br_poly[i].nextpoly
            if  i == 0:    #end of loop over polymers
                break
        fout.close()


    def multipolyconfwrite(self, Fname, weights, inmix, numsaved):
        """version for mixtures"""
        # var i,atally,numarms,anum,n,nmix:integer
        #     first,tL1, tL2, tR1, tR2, m1,mc, npoly: integer
        #     F: TextFile
        #     enrich,polywt,armwt,armz,N_e,N_e_av,distwt:double

        # count polymers over all distributions
        numsaved = 0
        nmix = 0
        N_e_av = 0

        for n in range(1, 11):
            if inmix[n - 1]:
                polybits.react_dist[n].N_e = polybits.react_dist[n].M_e / polybits.react_dist[n].monmass
                N_e_av = N_e_av + polybits.react_dist[n].N_e
                nmix += 1
                numsaved = numsaved + polybits.react_dist[n].nsaved

        N_e_av = N_e_av/nmix

        # opening lines
        fout = open(Fname, 'w')

        fout.write('reactmix')
        fout.write('{0:12f}'.format(N_e_av))
        fout.write(numsaved)
        atally = 0

        # now loop through distributions writing output
        for n in range(1, 11):
            if inmix[n - 1]:
                distwt = weights[n - 1]

                # loop through polymers, writing output
                npoly = polybits.react_dist[n].npoly
                N_e = polybits.react_dist[n].N_e
                i = polybits.react_dist[n].first_poly
                while True:
                    if polybits.br_poly[i].saved:
                        if polybits.react_dist[n].numinbin[polybits.br_poly[i].bin] <= polybits.react_dist[n].bobbinmax:
                            enrich = 1.0
                        else:
                            enrich = polybits.react_dist[n].numinbin[polybits.br_poly[i].bin] / polybits.react_dist[n].bobbinmax
                        polywt = enrich / npoly * distwt

                        if polybits.br_poly[i].num_br == 0: #it's a linear polymer
                            fout.write(2)
                            atally = atally + 2
                            first = polybits.br_poly[i].first_end
                            armwt = 0.5*polybits.arm_pool[first].arm_len / polybits.br_poly[i].tot_len * polywt
                            armz = 0.5*polybits.arm_pool[first].arm_len / N_e
                            fout.write('-1 -1 1 -1 {:12f} {:15f}'.format(armz, armwt))
                            fout.write('0 -1 -1 -1 {:12f} {:15f}'.format(armz, armwt))

                        else: # it's a branched polymer
                            numarms = 2*polybits.br_poly[i].num_br + 1
                            fout.write(numarms)  #number of arms
                            atally = atally + numarms
                            first = polybits.br_poly[i].first_end

                            #renumber segments starting from zero
                            m1 = first
                            anum = 0
                            while True:
                                polybits.arm_pool[m1].armnum = anum
                                m1 = polybits.arm_pool[m1].down
                                anum = anum + 1
                                if m1 == first:
                                    break

                            # now do output - loop over arms
                            m1 = first
                            while True:
                                armwt = polybits.arm_pool[m1].arm_len / polybits.br_poly[i].tot_len * polywt
                                armz = polybits.arm_pool[m1].arm_len / N_e
                                if polybits.arm_pool[m1].L1 == 0:
                                    tL1 = -1
                                else:
                                    mc = np.abs(polybits.arm_pool[m1].L1)
                                    tL1 = polybits.arm_pool[mc].armnum

                                if polybits.arm_pool[m1].L2 == 0:
                                    tL2 = -1
                                else:
                                    mc = np.abs(polybits.arm_pool[m1].L2)
                                    tL2 = polybits.arm_pool[mc].armnum

                                if polybits.arm_pool[m1].R1 == 0:
                                    tR1 = -1
                                else:
                                    mc = np.abs(polybits.arm_pool[m1].R1)
                                    tR1 = polybits.arm_pool[mc].armnum

                                if polybits.arm_pool[m1].R2 == 0:
                                    tR2 = -1
                                else:
                                    mc = np.abs(polybits.arm_pool[m1].R2)
                                    tR2 = polybits.arm_pool[mc].armnum

                                fout.write(tL1, tL2, tR1, tR2, '{:12f} {:15f}'.format(armz, armwt))

                                m1 = polybits.arm_pool[m1].down

                                if m1 == first:  #end output loop over arms
                                    break
                        # end of if (it's a linear or branched polymer )
                    #end of "if saved"
                    i = polybits.br_poly[i].nextpoly
                    if i == 0:    #end of loop over polymers
                        break
            # end of loop over distributions
        fout.close()

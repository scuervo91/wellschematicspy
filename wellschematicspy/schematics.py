
# Source Code taken and modified from:
#https://github.com/kinverarity1/well-schematics
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import transforms as mtransforms
import numpy as np
from pydantic import BaseModel, Extra, Field
from pydantic.color import Color
from typing import List, Optional, Union

#local imports 

from .models import BridgePlug, OpenHole, Casing, Cement, Perforation, Sleeve, Packer,Plug, BridgePlug, Tubing


class WellSchema(BaseModel):
    open_holes: List[OpenHole]  = Field(...)
    casings: Optional[List[Casing]]  = Field(None)
    completion: Optional[List[Union[Sleeve, Packer,Plug, BridgePlug, Tubing]]]  = Field(None)
    
    class Config:
        validate_assignment = True
        extra = Extra.forbid
        arbitrary_types_allowed = True
        
    def list_diameter(self):
        d = []

        d.extend([o.diameter for o in self.open_holes])
        if self.casings:
            d.extend([c.diameter for c in self.casings])
        if self.completion:
            d.extend([m.diameter for m in self.completion])
        
        return np.array(d)     
    
    def max_diameter(self):
        return self.list_diameter().max()

    def unique_diameter(self):
        return np.unique(self.list_diameter())
        
    def top(self):
        d = []

        d.extend([o.top for o in self.open_holes])
        if self.casings:
            d.extend([c.top for c in self.casings])
        if self.completion:
            d.extend([m.top for m in self.completion])
        
        return np.array(d).min()
    
    def bottom(self):
        d = []

        d.extend([o.bottom for o in self.open_holes])
        if self.casings:
            d.extend([c.bottom for c in self.casings])
        if self.completion:
            d.extend([m.bottom for m in self.completion])
        
        return np.array(d).max()
    
    def plot(self,
        ax=None,
        tight_layout=True,
        dtick=True,
        xtick = False,
        lims=None,
        fontsize=8,
        which:list=['open_hole','casing','completion']
    ):
        if ax is None:
            fig = plt.figure(figsize=(4, 9))
            ax = fig.add_subplot(111)

        t = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
        patches = []

        di_factor = self.max_diameter()

        #Open Hole
        if 'open_hole' in which:
            for o in self.open_holes:
                top = o.top
                bottom = o.bottom
                length = bottom - top
                diameter = o.diameter
                color = o.color.as_hex()
                hatch = o.hatch
                oh_patch = mpatches.Rectangle(
                    (0.5*(1-diameter/di_factor), top),
                    (0.5*(1+diameter/di_factor)) - (0.5*(1-diameter/di_factor)),
                    length,
                    facecolor=color,
                    transform=t,
                    hatch = hatch
                )
                patches.append(oh_patch)
                
        if self.casings is not None and 'casing' in which:
            for c in self.casings:
                top = c.top
                bottom = c.bottom
                length = bottom - top
                diameter = c.diameter
                pipe_width= c.pipe_width
                shoe_scale= c.shoe_scale
                color = c.color.as_hex()

                xl =  0.5*(1-diameter/di_factor)
                xr =  0.5*(1+diameter/di_factor)
                seg_left = mpatches.Rectangle(
                    (xl, top), 
                    pipe_width, 
                    length, 
                    facecolor=color,
                    transform=t,
                )
                seg_right = mpatches.Rectangle(
                    (xr-pipe_width, top),
                    pipe_width,
                    length,
                    facecolor=color,
                    transform=t,
                )
                #Shoe
                left_shoe = np.array([[xl,0],[xl,-1*shoe_scale],[xl-pipe_width,0]])
                left_shoe[:,1] = left_shoe[:,1] + bottom
                right_shoe = np.array([[xr,0],[xr,-1*shoe_scale],[xr+pipe_width,0]])
                right_shoe[:,1] = right_shoe[:,1] + bottom
                ls = mpatches.Polygon(left_shoe, color='k')
                rs = mpatches.Polygon(right_shoe, color='k')

                patches.extend([seg_left,seg_right,ls,rs])
    
                if c.cement:
                    for cem in c.cement:
                        cement_color = cem.color.as_hex()
                        cement_hatch = cem.hatch
                        cement_oh = cem.oh
                        cement_top = cem.top
                        cement_bottom = cem.bottom

                        cl =  0.5*(1-cement_oh/di_factor)
                        cement_width = xl - cl
                        cement_length = cement_bottom - cement_top

                        cem_left = mpatches.Rectangle(
                            (cl, cement_top), 
                            cement_width, 
                            cement_length, 
                            facecolor=cement_color,
                            transform=t,
                            hatch = cement_hatch
                        )

                        cem_right = mpatches.Rectangle(
                            (xr, cement_top), 
                            cement_width, 
                            cement_length, 
                            facecolor=cement_color,
                            transform=t,
                            hatch = cement_hatch
                        )
                        patches.extend([cem_left,cem_right])

                if c.perforations:
                    for perf in c.perforations:
                        perf_color = perf.color.as_hex()
                        perf_hatch = perf.hatch
                        perf_scale = perf.scale
                        perf_penetrate = perf.penetrate
                        perf_oh = perf.oh
                        perf_top = perf.top
                        perf_bottom = perf.bottom

                        pl =  0.5*(1-perf_oh*perf_penetrate/di_factor)
                        pr =  0.5*(1+perf_oh*perf_penetrate/di_factor)
                        
                        for i in np.arange(perf_top,perf_bottom,perf_scale):
                            left_perf = np.array([[pl,perf_scale/2],[xl,perf_scale],[xl,0]])
                            left_perf[:,1] = left_perf[:,1] + i
                            right_perf = np.array([[pr,perf_scale/2],[xr,perf_scale],[xr,0]])
                            right_perf[:,1] = right_perf[:,1] + i

                            lp = mpatches.Polygon(
                                left_perf, 
                                color=perf_color,
                                hatch=perf_hatch
                            )
                            rp = mpatches.Polygon(
                                right_perf, 
                                color=perf_color,
                                hatch=perf_hatch
                            )
                            patches.extend([lp,rp])
    
        if self.completion is not None and 'completion' in which:
            for c in self.completion:
                top = c.top
                bottom = c.bottom
                length = bottom - top
                diameter = c.diameter
                color = c.color.as_hex()
                hatch = c.hatch

                xl =  0.5*(1-diameter/di_factor)
                xr =  0.5*(1+diameter/di_factor)

                if isinstance(c,Tubing):
                    pipe_width=c.pipe_width
                    seg_left = mpatches.Rectangle(
                        (xl, top), 
                        pipe_width, 
                        length, 
                        facecolor=color,
                        transform=t,
                    )
                    seg_right = mpatches.Rectangle(
                        (xr-pipe_width, top),
                        pipe_width,
                        length,
                        facecolor=color,
                        transform=t,
                    )

                    patches.extend([seg_left,seg_right])

                if isinstance(c,Packer):
                    inner_diameter = c.inner_diameter
                    xli =  0.5*(1-inner_diameter/di_factor)
                    width = xli - xl
                    seg_left = mpatches.Rectangle(
                        (xl, top), 
                        width, 
                        length, 
                        facecolor=color,
                        transform=t,
                        hatch = hatch
                    )
                    seg_right = mpatches.Rectangle(
                        (xr-width, top),
                        width,
                        length,
                        facecolor=color,
                        transform=t,
                        hatch = hatch
                    )

                    patches.extend([seg_left,seg_right])
                
                elif isinstance(c,(BridgePlug,Sleeve,Plug)):
                    oh_patch = mpatches.Rectangle(
                        (0.5*(1-diameter/di_factor), top),
                        (0.5*(1+diameter/di_factor)) - (0.5*(1-diameter/di_factor)),
                        length,
                        facecolor=color,
                        transform=t,
                        hatch = hatch
                    )
                    patches.append(oh_patch)



        for patch in patches:
            ax.add_artist(patch)

        ax.grid(False)
        for side in ["left", "right", "bottom", "top"]:
            ax.spines[side].set_visible(True)
        if not dtick:
            ax.yaxis.set_ticks_position("none")
        #ax.set_facecolor("white")
        if xtick:
            di = self.unique_diameter()
            ax.set_xticks(np.concatenate([0.5*(1-di/di_factor),0.5*(1+di/di_factor)]))
            ax.set_xticklabels(np.around(np.concatenate([di,di]),decimals=1))
        else:
            ax.set_xticklabels([])
        ax.xaxis.set_label_position("top")
        ax.xaxis.tick_top()
        ax.set_xlim([0,1])
        ax.set_xlabel('Well Schematic')
        ax.tick_params("both",labelsize=fontsize)
        if lims is None:
            ax.set_ylim([self.bottom(),self.top()])
        else:
            ax.set_ylim([lims[1],lims[0]])

        if tight_layout:
            ax.figure.tight_layout()

        #return patches
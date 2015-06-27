if PlotType==1
  rybcolormap
  caxis([-.1 .1])
  colorbar
end

showpatchborders

hold on
plot([0.5 0.5],[0 1],'w','linewidth',3);
hold off
zl = zlim;
set(gca,'zlim',[zl(1) 0]);

axis square

clear afterframe;

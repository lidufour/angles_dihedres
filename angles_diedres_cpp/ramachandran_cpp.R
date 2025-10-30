# extraction des données des angles dièdres calculés

diedre_start <- read.csv(file = "./angles_start.csv")
angles_phi <- as.numeric(diedre_start$Angle.phi)
angles_psi <- as.numeric(diedre_start$Angle.psi)

# plot sous forme de diagramme de ramachandran

plot(angles_phi, # valeurs des abscisses
     angles_psi, # valeurs des ordonnées
     col = "red",
     pch = 20,
     panel.first = grid(nx = 6, ny = 6), # quadrillage du plot
     xlim = c(-180,180), # min et max de l'axe des abscisses
     ylim = c(-180,180), # min et max de l'axe des ordonnées
     xaxp = c(-180, 180, 6), # espacement de la graduation des x
     yaxp = c(-180,180, 6), # espacement de la graduation des y
     
     main = "Diagramme de Ramachandran de la CPP",
     xlab = "angle phi (degrés)",
     ylab = "angle psi (degrés)",
     
     # pour que xmin et ymin se confondent à l'intersection des axes:
     yaxs="i", xaxs = "i")

diedre_md <- read.csv(file = "./angles_md.csv")
angles_phi_md <- as.numeric(diedre_md$Angle.phi)
angles_psi_md <- as.numeric(diedre_md$Angle.psi)

points(angles_phi_md,
       angles_psi_md,
       col = "blue",
       pch = 20)


# ajout des données calculées par biopython

diedre_start.biopy <- read.csv(file = "./Angles_biopython_start.csv")
diedre_md.biopy <- read.csv(file = "./Angles_biopython_md.csv")

phi_start.biopy <- as.numeric(diedre_start.biopy$Angle.phi)
psi_start.biopy <- as.numeric(diedre_start.biopy$Angle.psi)

points(phi_start.biopy,
       psi_start.biopy,
       col = "red",
       pch = 0)

# stockage des données des angles phi et psi md de biopython
phi_md.biopy <- as.numeric(diedre_md.biopy$Angle.phi)
psi_md.biopy <- as.numeric(diedre_md.biopy$Angle.psi)

# tracé des points représentants les angles phi et psi md de biopython
points(phi_md.biopy,
       psi_md.biopy,
       col = "blue",
       pch = 0)

# ajout de la légende
legend("bottomleft",
  legend = c("start (fct_calculs_diedres)", "md (fct_calcul_diedres)",
             "start (BioPython)", "md (BioPython)"),
  col = c("red","blue","red","blue"),
  pch = c(20,20,0,0),
  cex = 0.9
)

dev.print(device = png, file = "ramachandran_cpp.png", width = 1000)


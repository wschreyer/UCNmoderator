#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <array>
#include "TGraph2D.h"

void DrawGeometry(const std::array<std::vector<double>, 4> &lv, double zmax){
  double xmin = min(*std::min_element(lv[0].begin(), lv[0].end()), *std::min_element(lv[2].begin(), lv[2].end()));
  double xmax = max(*std::max_element(lv[0].begin(), lv[0].end()), *std::max_element(lv[2].begin(), lv[2].end()));
  double ymin = min(*std::min_element(lv[1].begin(), lv[1].end()), *std::min_element(lv[3].begin(), lv[3].end()));
  double ymax = max(*std::max_element(lv[1].begin(), lv[1].end()), *std::max_element(lv[3].begin(), lv[3].end()));
  double xscale = 200/(xmax - xmin);
  double yscale = (zmax + 30)/(ymax - ymin);

  for (int i = 0; i < lv[0].size(); ++i){
    TLine *l = new TLine((lv[0][i] - xmin)*xscale - 100, (lv[1][i] - ymin)*yscale - 30, (lv[2][i] - xmin)*xscale - 100, (lv[3][i] - ymin)*yscale - 30);
    l->Draw();
  }
}

void DrawPlot(TGraph2D *gr, std::vector<double> &xv, std::vector<double> &yv, std::vector<double> &vv, const std::string &title){
  gr->SetTitle(title.c_str());
  gr->SetNpx(100);
  gr->SetNpy(70);
  gr->GetHistogram();
  gr->GetXaxis()->SetTitle("x (cm)");
  gr->GetXaxis()->SetLimits(-100.,100.);
  gr->GetYaxis()->SetTitle("z (cm)");
  gr->GetYaxis()->SetLimits(-30.,110.);
  gr->Draw("COL1Z");
}

void plot(){
  std::ifstream f("MESHTALMRG");
  std::vector<double> xv, zv, vv;
  while (f){
    std::string line;
    getline(f, line);
    std::istringstream str(line);
    double x, y, z, v, dv;
    str >> x >> y >> z >> v >> dv;
    if (str){
      xv.push_back(x);
      zv.push_back(z);
      vv.push_back(v*6.2415e12);
    }
  }
  f.close();
  
  f.open("plotm.ps");
  std::array<std::vector<double>, 4> lv;
  while (f){
    std::string line;
    getline(f, line);
    std::istringstream str(line);
    double x1, y1, x2, y2;
    std::string c1, c2;
    str >> x1 >> y1 >> c1 >> x2 >> y2 >> c2;
    if (str && c1 == "moveto" && c2 == "lineto"){
      lv[0].push_back(x1);
      lv[1].push_back(y1);
      lv[2].push_back(x2);
      lv[3].push_back(y2);
    }
  }
  f.close();
  
  f.open("ucn.mcnp");
  double zmax;
  while (f){
    std::string line;
    getline(f, line);
    std::istringstream str(line);
    int cell;
    std::string cname;
    str >> cell >> cname >> zmax >> zmax >> zmax >> zmax >> zmax >> zmax;
    if (str && cell == 21){
      assert(cname == "RPP");
      break;
    }
    else if (!f)
      throw std::runtime_error("Uppermost cell (reflecto) not found!");
  }

  TCanvas c("c", "c", 800, 600);
  c.SetRightMargin(0.12);
  TGraph2D *gr = new TGraph2D(7000, &xv[0], &zv[0], &vv[0]);
  DrawPlot(gr, xv, zv, vv, "Neutron flux <6 meV");
  DrawGeometry(lv, zmax);
  c.Update();
  c.Print("n20K.pdf");
  gr = new TGraph2D(7000, &xv[7000], &zv[7000], &vv[7000]);
  DrawPlot(gr, xv, zv, vv, "Neutron flux 6-100 meV");
  DrawGeometry(lv, zmax);
  c.Print("n300K.pdf");
  c.SetLogz();
  gr = new TGraph2D(7000, &xv[14000], &zv[14000], &vv[14000]);
  DrawPlot(gr, xv, zv, vv, "Neutron flux >100 meV");
  DrawGeometry(lv, zmax);
  c.Print("nfast.pdf");
}


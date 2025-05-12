v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 490 -220 490 -200 {lab=GND}
N 490 -300 490 -280 {lab=vdd}
N 320 -290 340 -290 {lab=vin}
N 320 -330 320 -290 {lab=vin}
N 170 -330 320 -330 {lab=vin}
N 170 -330 170 -290 {lab=vin}
N 170 -290 200 -290 {lab=vin}
N 240 -240 240 -210 {lab=vcm_in}
N 310 -210 380 -210 {lab=vcm_in}
N 380 -240 380 -210 {lab=vcm_in}
N 310 -130 310 -110 {lab=GND}
N 310 -210 310 -190 {lab=vcm_in}
N 240 -210 310 -210 {lab=vcm_in}
N 90 -290 90 -280 {lab=vin}
N 90 -290 170 -290 {lab=vin}
N 240 -370 240 -300 {lab=vinp}
N 380 -370 380 -300 {lab=vinn}
N 490 -140 490 -120 {lab=vss}
N 1130 -520 1130 -500 {lab=vss}
N 1030 -810 1030 -780 {lab=#net1}
N 1230 -810 1230 -780 {lab=#net2}
N 1030 -910 1030 -870 {lab=vout1p}
N 1230 -910 1230 -870 {lab=vout1n}
N 1030 -990 1030 -970 {lab=vdd}
N 1230 -990 1230 -970 {lab=vdd}
N 1130 -610 1130 -580 {lab=v_deg1}
N 1070 -640 1090 -640 {lab=vnbias}
N 970 -840 990 -840 {lab=vinp}
N 1270 -840 1300 -840 {lab=vinn}
N 1030 -990 1230 -990 {lab=vdd}
N 1130 -780 1150 -780 {lab=#net3}
N 1210 -780 1230 -780 {lab=#net2}
N 1130 -780 1130 -670 {lab=#net3}
N 1030 -780 1050 -780 {lab=#net1}
N 1110 -780 1130 -780 {lab=#net3}
N 690 -570 690 -530 {lab=vnbias}
N 780 -570 780 -500 {lab=vnbias}
N 730 -500 780 -500 {lab=vnbias}
N 690 -570 780 -570 {lab=vnbias}
N 690 -670 690 -650 {lab=vdd}
N 690 -590 690 -570 {lab=vnbias}
N 690 -470 690 -440 {lab=v_deg}
N 690 -380 690 -360 {lab=vss}
C {devices/title.sym} 245 -55 0 0 {name=l5 author="Patrick Fath"}
C {launcher.sym} 970 -175 0 0 {name=h3
descr=SimulateNGSPICE
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# run netlist and simulation
xschem netlist
simulate
"}
C {devices/vsource.sym} 490 -250 0 0 {name=VDD1 value=3.3}
C {devices/vsource.sym} 490 -170 0 0 {name=VSS1 value=0}
C {gnd.sym} 490 -210 1 0 {name=l3 lab=GND}
C {vcvs.sym} 240 -270 0 0 {name=E1 value=0.5}
C {vcvs.sym} 380 -270 0 0 {name=E2 value=-0.5}
C {gnd.sym} 340 -250 0 0 {name=l1 lab=GND}
C {gnd.sym} 200 -250 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 310 -160 0 0 {name=VCM_IN1 value=2.2}
C {gnd.sym} 310 -110 0 0 {name=l4 lab=GND}
C {devices/vsource.sym} 90 -250 0 0 {name=VIN1 value="dc 0 ac 1 sin(0 \{sine_in_amp\} \{sine_in_freq\})"}
C {gnd.sym} 90 -220 0 0 {name=l6 lab=GND}
C {devices/launcher.sym} 970 -135 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {lab_wire.sym} 240 -370 0 1 {name=p5 sig_type=std_logic lab=vinp}
C {lab_wire.sym} 380 -370 0 1 {name=p6 sig_type=std_logic lab=vinn}
C {lab_wire.sym} 260 -210 0 1 {name=p12 sig_type=std_logic lab=vcm_in}
C {lab_wire.sym} 100 -290 0 1 {name=p13 sig_type=std_logic lab=vin}
C {lab_wire.sym} 490 -300 0 1 {name=p1 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 490 -120 0 1 {name=p3 sig_type=std_logic lab=vss}
C {vcvs.sym} 1935 -170 0 0 {name=E3 value=1}
C {lab_wire.sym} 1895 -150 0 0 {name=p19 sig_type=std_logic lab=vout1n}
C {lab_wire.sym} 1895 -190 0 0 {name=p20 sig_type=std_logic lab=vout1p}
C {gnd.sym} 1935 -140 0 0 {name=l7 lab=GND}
C {lab_wire.sym} 1935 -200 0 1 {name=p21 sig_type=std_logic lab=vout_diff}
C {code_shown.sym} 1515 -215 0 0 {
name=TT_MODELS
only_toplevel=true
value="
** IHP models
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerHBT.lib hbt_typ
.lib cornerRES.lib res_typ
"
spice_ignore=false
      }
C {simulator_commands_shown.sym} 85 -865 0 0 {name=OPT_AC
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.param R1_val=500
.param R2_val=30
.param R3_val=100
.param sine_in_amp=0
.param sine_in_freq=100k
.control

save all
ac dec 1001 10k 1T
let gain_lin = abs(vout_diff)
let gain_dB = vdb(vout_diff)
let gain_dc_dB = gain_dB[0]
meas ac gain_1GHz_dB FIND gain_dB AT=1G 
let gain_fc_dB = gain_dc_dB-3
meas ac fc when gain_dB = gain_fc_dB
let GBW = gain_lin[0] * fc
echo results_opt_start
print gain_dc_dB
print gain_1Ghz_dB
print fc
print GBW
echo results_opt_end
.endc
"
}
C {simulator_commands_shown.sym} 1685 -935 0 0 {name=OP_AC_TRAN
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.param R1_val=500
.param R2_val=30
.param R3_val=100
.param sine_in_amp=1m
.param sine_in_freq=10k
.include fd_amp.save
.control

save all
op
write fd_amp.raw
set appendwrite
ac dec 1001 10k 1T
write fd_amp.raw
let gain_lin = abs(vout_diff)
let gain_dB = vdb(vout_diff)
let gain_dc_dB = gain_dB[0]
meas ac gain_1GHz_dB FIND gain_dB AT=1G 
let gain_fc_dB = gain_dc_dB-3
meas ac fc when gain_dB = gain_fc_dB
let GBW = gain_lin[0] * fc
print gain_dc_dB
print gain_1Ghz_dB
print fc
print GBW
plot gain_dB xlimit 10k 1T ylabel 'small signal gain'
tran 0.1u 100u
write fd_amp.raw
plot vout_diff
.endc
"
spice_ignore=true}
C {lab_wire.sym} 970 -840 0 0 {name=p55 sig_type=std_logic lab=vinp}
C {sg13g2_pr/npn13G2.sym} 1010 -840 0 0 {name=Q3
model=npn13G2
spiceprefix=X
Nx=1
}
C {sg13g2_pr/npn13G2.sym} 1250 -840 0 1 {name=Q4
model=npn13G2
spiceprefix=X
Nx=1
}
C {res.sym} 1130 -550 0 0 {name=R2
value=\{R2_val\}
footprint=1206
device=resistor
m=1}
C {sg13g2_pr/npn13G2.sym} 1110 -640 0 0 {name=Q2
model=npn13G2
spiceprefix=X
Nx=1
}
C {lab_wire.sym} 1130 -500 0 0 {name=p8 sig_type=std_logic lab=vss}
C {lab_wire.sym} 1130 -590 0 0 {name=p16 sig_type=std_logic lab=v_deg1}
C {sg13g2_pr/annotate_bip_params.sym} 1190 -670 0 0 {name=annot2 ref=Q2}
C {res.sym} 1030 -940 0 0 {name=R3
value=\{R1_val\}
footprint=1206
device=resistor
m=1}
C {res.sym} 1230 -940 0 0 {name=R4
value=\{R1_val\}
footprint=1206
device=resistor
m=1}
C {lab_wire.sym} 1130 -640 2 0 {name=p27 sig_type=std_logic lab=vss}
C {lab_wire.sym} 1230 -840 2 1 {name=p9 sig_type=std_logic lab=vss}
C {lab_wire.sym} 1030 -840 2 0 {name=p28 sig_type=std_logic lab=vss}
C {lab_wire.sym} 1070 -640 0 0 {name=p32 sig_type=std_logic lab=vnbias}
C {lab_wire.sym} 1120 -990 0 1 {name=p10 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 1300 -840 0 1 {name=p11 sig_type=std_logic lab=vinn}
C {lab_wire.sym} 1030 -880 0 1 {name=p14 sig_type=std_logic lab=vout1p}
C {lab_wire.sym} 1230 -880 0 0 {name=p15 sig_type=std_logic lab=vout1n}
C {res.sym} 1080 -780 1 0 {name=R1
value=\{R3_val\}
footprint=1206
device=resistor
m=1}
C {res.sym} 1180 -780 1 0 {name=R5
value=\{R3_val\}
footprint=1206
device=resistor
m=1}
C {sg13g2_pr/annotate_bip_params.sym} 790 -890 0 0 {name=annot1 ref=Q3}
C {sg13g2_pr/annotate_bip_params.sym} 1440 -890 0 0 {name=annot3 ref=Q4}
C {sg13g2_pr/npn13G2.sym} 710 -500 0 1 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
}
C {isource.sym} 690 -620 0 0 {name=I0 value=1m}
C {sg13g2_pr/annotate_bip_params.sym} 750 -470 0 0 {name=annot4 ref=Q1}
C {res.sym} 690 -410 0 0 {name=R6
value=\{R2_val\}
footprint=1206
device=resistor
m=1}
C {lab_wire.sym} 690 -450 0 0 {name=p26 sig_type=std_logic lab=v_deg}
C {lab_wire.sym} 690 -500 2 1 {name=p34 sig_type=std_logic lab=vss}
C {lab_wire.sym} 780 -570 0 1 {name=p17 sig_type=std_logic lab=vnbias}
C {lab_wire.sym} 690 -670 0 1 {name=p18 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 690 -360 0 1 {name=p22 sig_type=std_logic lab=vss}

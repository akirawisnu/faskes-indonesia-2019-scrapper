clear
clear matrix
set more off
cap ssc install egenmore

gl path "C:\Users\Akirawisnu\Documents\work\faskes"
cap mkdir out "$path/cleaned"

cap rm data_0.dta
local file: dir "$path" file "*.dta"

foreach i in `file'{
	local x: subinstr local i ".dta" "", all
	local x: subinstr local x "data_" "", all
	di "`x'"
	
	use "$path/`i'" , clear
	count
	if r(N)==0{
		di "no file detected"
		}
	else{
		drop index

		ren _0 a
		replace a=subinstr(a,"]Index: []","",.)
		replace a=subinstr(a,"] Index: []","",.)
		replace a=subinstr(a,"Index: []","",.)
		replace a=subinstr(a,"Empty DataFrame","",.)
		replace a=subinstr(a,"Columns: [","",.)
		replace a=subinstr(a,"]","",.)

		replace a=subinstr(a,", '","|",.)
		replace a=subinstr(a,"'","",.)
		replace a=subinstr(a," Medis","",.)
		split a, parse("|")
		drop a
		
		des
		if r(k)>21{
			forval j=1/14{
				local k=8+`j'
				local l=`k'-1
				replace a`l'=a`k'
				}
			drop a22
			}

		ds a8-a21
		foreach i in `r(varlist)'{
			destring `i', replace
			replace `i'=floor(`i')
			}

		egen kode_prov=sieve(a1), char(0123456789)
		drop a1
		ren a2 lat_
		ren a3 long_
		ren a4 title
		ren a5 kode_faskes
		ren a6 nama_faskes
		ren a7 alamat_faskes
		ren a8 medis
		ren a9 psikologi_klinis
		ren a10 perawat
		ren a11 bidan
		ren a12 farmasi
		ren a13 kesmas
		ren a14 kesling
		ren a15 gizi
		ren a16 terapi_fisik
		ren a17 teknisi_medis
		ren a18 teknik_biomed
		ren a19 kes_tradisional
		ren a20 nakes_lain
		ren a21 penunjang

		order kode_prov
		compress
		tempfile a`x'
		saveold `a`x'', replace
		}
	}
	
cap drop _all
foreach i in `file'{
	local x: subinstr local i ".dta" "", all
	local x: subinstr local x "data_" "", all
	di "`x'"
	
	append using `a`x'', force
	}
	
compress
saveold "$path/cleaned/finfile_faskes_indonesia_2019.dta", replace	
	
exit

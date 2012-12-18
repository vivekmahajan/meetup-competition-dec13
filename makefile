all:
	rm -rf output
	python decoder.py input_rule decoder_input.txt 50 0.5 5 20 
	#python decoder.py phrase-table decoder_input.txt 50 0.5 5 20 
	#50 is the beam size; 0.5 is alpha; 5 is the distortion limit; 50 best translations
debug:
	rm -rf output	
	python decoder.py phrase-table temp 50 0.5 5 20 > output
	#50 is the beam size; 0.5 is alpha; 5 is the distortion limit; 20 best translations

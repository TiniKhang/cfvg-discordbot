about = "cfvg-bot is a discord bot made by LittleFighterFox with a set of commands that is useful for discussing cardfight vanguard. Currently supporting mathematical probability calcuations, it should soon be extended to have automatic searching of cards. Project can found at https://github.com/NanoSmasher/cfvg-discordbot"

helping = {
	"eval": '''vbot eval [*]
Evaluates expression supporting BEDMAS operations, probabilities (AND,OR,XOR) and Geometric Distribution of at least 1 (!a,b,c,d)
#NOTE: Population size and Sample size swapped for all other functions
	a := Sample size
	b := Possible successes
	c := Population size
	d := Number of successes	
	''',
	"hgcc": '''vbot hgcc [*1] [*2] [*3] [*4] [*5]
Hyper Geometric Cumulative Calculator
	*1 := Population size
	*2 := Possible successes
	*3 := Sample size
	*4 := Number of successes
	*5 := Available inputs (no quotes): '<' , '<=' , '>' , '>=' , '='
	''',
	"quickodds": '''vbot quickodds [*1] [*2] [*3] [*4]
Displays all probabilities of a given value
    a: Population size
    b: Possible successes
    c: Sample size
    d: # of successes
	''',
	"cascadeodds": '''vbot cascadeodds [*1] [*2] [*3]
Print exact odds for each # of successes
	*1 := Population size
	*2 := Possible successes
	*3 := Sample size
	'''
}
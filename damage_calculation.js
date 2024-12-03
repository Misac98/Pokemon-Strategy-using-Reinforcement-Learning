const { Generations, Pokemon, Move, calculate, Field } = require('@smogon/calc');

const gen = Generations.get(2);

function calculateDamage(attackerName, attackerLevel, attackerItem, attackerStatus, attackerAbility, attackerBoosts,
    defenderName, defenderLevel, defenderItem, defenderStatus, defenderAbility, defenderBoosts,
    moveName) {
    const attacker = new Pokemon(gen, attackerName, {
        /*
        evs: {hp: 85, atk: 85, def: 85, spa: 85, spd: 85, spe: 85},
        ivs: {hp: 31, atk: 31, def: 31, spa: 31, spd: 31, spe: 31},
        nature: 'Jolly',
        */
        level: attackerLevel,
        item: attackerItem,
        ability: attackerAbility,
        boosts: attackerBoosts,
        status: attackerStatus
    });
    const defender = new Pokemon(gen, defenderName, {
        /*
        evs: { hp: 85, atk: 85, def: 85, spa: 85, spd: 85, spe: 85 },
        ivs: { hp: 31, atk: 31, def: 31, spa: 31, spd: 31, spe: 31 },
        nature: 'Calm',
        */
        level: defenderLevel,
        item: defenderItem,
        ability: defenderAbility,
        boosts: defenderBoosts,
        status: defenderStatus
    });
    const move = new Move(gen, moveName);
    const field = new Field();

    const result = calculate(gen, attacker, defender, move, field);

    return result.damage;  // Returns an array with possible damage values
}


// arg1 = 'Gengar'
// arg2 = '100'
// arg3 = 'leftovers'
// arg4 = 'None'
// arg5 = 'noability'
// arg6 = "{'accuracy': 0, 'atk': 0, 'def': 0, 'evasion': 0, 'spa': 0, 'spd': 0, 'spe': 0}"
//
// arg7 = 'Chansey'
// arg8 = '100'
// arg9 = 'leftovers'
// arg10 = 'None'
// arg11 = 'noability'
// arg12 = "{'accuracy': 0, 'atk': 0, 'def': 0, 'evasion': 0, 'spa': 0, 'spd': 0, 'spe': 0}"
//
// arg13 = 'Thunderbolt'
// arg13 = 'Focus Blast'

// console.log(JSON.stringify(calculateDamage(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13)));


const args = process.argv.slice(2);
console.log(JSON.stringify(calculateDamage(args[0], args[1], args[2], args[3], args[4], args[5],
    args[6], args[7], args[8], args[9], args[10], args[11], args[12])));


/*
//Check if enough arguments are provided
if (args.length < 3) {
   console.error("Usage: node damage_calculation.js <attackerName> <defenderName> <moveName>");
   process.exit(1);
}

// Calculate damage and output the result as JSON string
try {
    console.log(JSON.stringify(calculateDamage(args[0], args[1], args[2])));
} catch (error) {
    console.error("Error calculating damage:", error.message);
}
*/


const express = require('express');
const apicache = require('apicache');
const { Generations, Pokemon, Move, calculate, Field } = require('@smogon/calc');
const app = express();
const port = require('./config.json').damage_calculator_server.port;

const cache = apicache.middleware;

function calculateDamage(generation, attackerName, attackerLevel, attackerItem, attackerStatus, attackerAbility, attackerBoosts,
    defenderName, defenderLevel, defenderItem, defenderStatus, defenderAbility, defenderBoosts,
    moveName) {
    const gen = Generations.get(generation);
    const attacker = new Pokemon(gen, attackerName, {
        level: attackerLevel,
        item: attackerItem,
        ability: attackerAbility,
        boosts: attackerBoosts,
        status: attackerStatus
    });
    const defender = new Pokemon(gen, defenderName, {
        level: defenderLevel,
        item: defenderItem,
        ability: defenderAbility,
        boosts: defenderBoosts,
        status: defenderStatus
    });
    const move = new Move(gen, moveName);
    const field = new Field();

    const result = calculate(gen, attacker, defender, move, field);
    return result;
}

app.use(express.json());

app.get('/calculate-damage', cache('5 minutes'), (req, res) => {
    const {
        generation, attackerName, attackerLevel, attackerItem, attackerStatus, attackerAbility, attackerBoosts,
        defenderName, defenderLevel, defenderItem, defenderStatus, defenderAbility, defenderBoosts,
        moveName
    } = req.query;

    const result = calculateDamage(
        generation, attackerName, attackerLevel, attackerItem, attackerStatus, attackerAbility, attackerBoosts,
        defenderName, defenderLevel, defenderItem, defenderStatus, defenderAbility, defenderBoosts,
        moveName
    );

    res.json(result.damage);
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
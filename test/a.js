let a = 2;

exports.plus = (one) => {
    a += 2;
    return one + a;
};

exports.minus = (one) => {
    return one - a;
};

// module.exports = function multi(one, two) {
//     return one * two;
// };

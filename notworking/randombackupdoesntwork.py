import csv
import itertools
from pickle import NONE
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    jointProbablity = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    for person in people:
        mother = people[person]["mother"]
        father = people[person]["father"]
        trait = people[person]["trait"]

        if mother == None and trait == None:
            if person in one_gene:
                jointProbablity[person]["gene"][1] = PROBS["gene"][1]
            elif person in two_genes:
                jointProbablity[person]["gene"][2] = PROBS["gene"][2]
            else:
                jointProbablity[person]["gene"][0] = PROBS["gene"][0]
            jointProbablity[person]["trait"][person in have_trait] = (PROBS["trait"][0][person in have_trait]*(PROBS["gene"][0]) +
                                                                      PROBS["trait"][1][person in have_trait] * (PROBS["gene"][1]) +
                                                                      PROBS["trait"][2][person in have_trait]*(PROBS["gene"][2]))

        elif mother != None:
            parent1GeneProbablity = 1.00
            parent2GeneProbablity = 1.00
            paren1Gene = 0
            paren2Gene = 0

            if mother in one_gene:
                paren1Gene = 1
            elif mother in two_genes:
                paren1Gene = 2

            if father in one_gene:
                paren2Gene = 1
            elif father in two_genes:
                paren2Gene = 2

            parent1trait = people[mother]["trait"]
            parent2trait = people[father]["trait"]
            parent1traitprobab = 1
            parent2traitprobab = 1
            if parent1trait != None:
                parent1traitprobab = PROBS["trait"][paren1Gene][people[mother]["trait"]]

            if parent2trait != None:
                parent2traitprobab = PROBS["trait"][paren2Gene][people[father]["trait"]]
            probablity = (PROBS["gene"][paren1Gene] * parent1traitprobab)*(
                PROBS["gene"][paren2Gene] * parent2traitprobab)

            if paren1Gene == 2:
                parent1GeneProbablity = 1-PROBS["mutation"]
            elif paren1Gene == 1:
                parent1GeneProbablity = (1-PROBS["mutation"]) * 0.50
            else:
                parent1GeneProbablity = PROBS["mutation"]

            if paren2Gene == 2:
                parent2GeneProbablity = 1-PROBS["mutation"]
            elif paren2Gene == 1:
                parent2GeneProbablity = (1-PROBS["mutation"]) * 0.50
            else:
                parent2GeneProbablity = PROBS["mutation"]

            if person in two_genes:
                probablity *= parent1GeneProbablity * parent2GeneProbablity
                jointProbablity[person]["gene"][2] = probablity
                jointProbablity[person]["trait"][person in have_trait] = PROBS["trait"][2][person in have_trait] * probablity

            elif person in one_gene:
                probablity *= (((1 - parent1GeneProbablity) * parent2GeneProbablity) +
                               (parent1GeneProbablity * (1 - parent2GeneProbablity)))
                jointProbablity[person]["gene"][1] = probablity
                jointProbablity[person]["trait"][person in have_trait] = PROBS["trait"][1][person in have_trait] * probablity

            else:
                probablity *= ((1 - parent1GeneProbablity) *
                               (1 - parent2GeneProbablity))
                jointProbablity[person]["gene"][0] = probablity
                jointProbablity[person]["trait"][person in have_trait] = PROBS["trait"][0][person in have_trait] * probablity

        else:

            if person in one_gene:
                jointProbablity[person]["gene"][1] = PROBS["trait"][1][people[person]
                                                                       ["trait"]] * PROBS["gene"][1]
            elif person in two_genes:
                jointProbablity[person]["gene"][2] = PROBS["trait"][2][people[person]
                                                                       ["trait"]] * PROBS["gene"][2]
            else:
                jointProbablity[person]["gene"][0] = PROBS["trait"][0][people[person]
                                                                       ["trait"]] * PROBS["gene"][0]
            jointProbablity[person]["trait"][person in have_trait] = people[person][
                "trait"] if person in have_trait else not people[person]["trait"]

    return jointProbablity


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in p:
        for gene in p[person]["gene"]:
            probabilities[person]["gene"][gene] += p[person]["gene"][gene]
        for trait in p[person]["trait"]:
            probabilities[person]["trait"][trait] += p[person]["trait"][trait]


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        sumGene = 0
        sumTrait = 0

        for gene in probabilities[person]["gene"]:
            sumGene += probabilities[person]["gene"][gene]

        for trait in probabilities[person]["trait"]:
            sumTrait += probabilities[person]["trait"][trait]

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene]/sumGene

        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait]/sumTrait


if __name__ == "__main__":
    main()

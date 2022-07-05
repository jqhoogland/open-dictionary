const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

const deleteAll = async () => {
    await prisma.definition.deleteMany().catch(console.error);
    await prisma.pronunciation.deleteMany().catch(console.error);
    await prisma.entry.deleteMany().catch(console.error);
    await prisma.sentence.deleteMany().catch(console.error);
    await prisma.sentenceTriple.deleteMany().catch(console.error);
}

deleteAll();
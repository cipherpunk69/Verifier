const fs = require('fs');
const path = require('path');

async function main() {
    const contract = 'Verifier.sol';
    const [contractData] = await hre.artifacts.readArtifact('Verifier.sol');

    const buildPath = path.resolve(__dirname, '../build');
    if (!fs.existsSync(buildPath)) fs.mkdirSync(buildPath);

    fs.writeFileSync(
        path.join(buildPath, 'Verifier.json'),
        JSON.stringify({ abi: contractData.abi, bytecode: contractData.bytecode }, null, 2)
    );

    console.log('Contract ABI and Bytecode have been compiled and saved!');
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});

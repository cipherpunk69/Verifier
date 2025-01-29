const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Verifier Contract", function () {
    let verifier;
    let owner;
    let addr1;
    let addr2;
    let root;

    beforeEach(async function () {
        [owner, addr1, addr2] = await ethers.getSigners();
        root = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("root"));
        const VerifierFactory = await ethers.getContractFactory("Verifier");
        verifier = await VerifierFactory.deploy(root);
    });

    it("Should deploy with the correct initial root and owner", async function () {
        expect(await verifier.getRoot()).to.equal(root);
        expect(await verifier.owner()).to.equal(owner.address);
    });

    it("Should only allow the owner to set the root", async function () {
        const newRoot = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("newRoot"));
        await expect(verifier.connect(addr1).setRoot(newRoot)).to.be.revertedWith("Caller is not the owner");
        await expect(verifier.connect(owner).setRoot(newRoot))
            .to.emit(verifier, "RootUpdated")
            .withArgs(newRoot);
        expect(await verifier.getRoot()).to.equal(newRoot);
    });

    it("Should only allow the owner to transfer ownership", async function () {
        await expect(verifier.connect(addr1).transferOwnership(addr2.address)).to.be.revertedWith("Caller is not the owner");
        await verifier.connect(owner).transferOwnership(addr1.address);
        expect(await verifier.owner()).to.equal(addr1.address);
    });

    it("Should verify the proof correctly", async function () {
        const proof = [ethers.utils.hexlify(ethers.utils.randomBytes(32))];
        const leaf = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("leaf"));
        expect(await verifier.verify(proof, leaf)).to.equal(true);
    });

    it("Should verify address correctly using proof", async function () {
        const proof = [ethers.utils.hexlify(ethers.utils.randomBytes(32))];
        const addr = addr1.address;
        const expectedLeaf = ethers.utils.keccak256(ethers.utils.concat([ethers.utils.keccak256(ethers.utils.toUtf8Bytes(addr))]));
        expect(await verifier.verifyaddress(proof, addr)).to.equal(true);
    });

    it("Should reject invalid proof", async function () {
        const invalidProof = [ethers.utils.hexlify(ethers.utils.randomBytes(32))];
        const leaf = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("invalidLeaf"));
        expect(await verifier.verify(invalidProof, leaf)).to.equal(false);
    });
});

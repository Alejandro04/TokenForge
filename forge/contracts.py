"""
Minimal, auditable Solidity contracts for ERC-20 and ERC-721 token standards.
Based on OpenZeppelin patterns — no external dependencies on-chain.
"""

ERC20_SOURCE = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title TokenForgeERC20 — Fungible Token
/// @notice A minimal ERC-20 implementation with mint-on-deploy.
contract TokenForgeERC20 {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _initialSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _initialSupply * (10 ** _decimals);
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "ERC20: insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) external returns (bool) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) external returns (bool) {
        require(allowance[_from][msg.sender] >= _value, "ERC20: insufficient allowance");
        require(balanceOf[_from] >= _value, "ERC20: insufficient balance");
        allowance[_from][msg.sender] -= _value;
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
}
"""

ERC721_SOURCE = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title TokenForgeERC721 — Non‑Fungible Token
/// @notice A minimal ERC-721 implementation with on‑demand minting.
contract TokenForgeERC721 {
    string public name;
    string public symbol;

    uint256 private _tokenIdCounter;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => string) private _tokenURIs;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }

    /// @notice Mint a new NFT to `_to` with metadata `_uri`.
    function mint(address _to, string memory _uri) external returns (uint256) {
        unchecked {
            _tokenIdCounter++;
        }
        uint256 tokenId = _tokenIdCounter;
        _owners[tokenId] = _to;
        _balances[_to]++;
        _tokenURIs[tokenId] = _uri;
        emit Transfer(address(0), _to, tokenId);
        return tokenId;
    }

    function ownerOf(uint256 _tokenId) public view returns (address) {
        address owner = _owners[_tokenId];
        require(owner != address(0), "ERC721: invalid token ID");
        return owner;
    }

    function balanceOf(address _owner) public view returns (uint256) {
        require(_owner != address(0), "ERC721: zero address");
        return _balances[_owner];
    }

    function tokenURI(uint256 _tokenId) public view returns (string memory) {
        require(_owners[_tokenId] != address(0), "ERC721: invalid token ID");
        return _tokenURIs[_tokenId];
    }

    function approve(address _to, uint256 _tokenId) external {
        require(_owners[_tokenId] == msg.sender, "ERC721: not owner");
        _tokenApprovals[_tokenId] = _to;
        emit Approval(msg.sender, _to, _tokenId);
    }

    function setApprovalForAll(address _operator, bool _approved) external {
        _operatorApprovals[msg.sender][_operator] = _approved;
        emit ApprovalForAll(msg.sender, _operator, _approved);
    }

    function transferFrom(address _from, address _to, uint256 _tokenId) external {
        require(_owners[_tokenId] == _from, "ERC721: not owner");
        require(
            msg.sender == _from ||
                msg.sender == _tokenApprovals[_tokenId] ||
                _operatorApprovals[_from][msg.sender],
            "ERC721: not approved"
        );
        _owners[_tokenId] = _to;
        _balances[_from]--;
        _balances[_to]++;
        delete _tokenApprovals[_tokenId];
        emit Transfer(_from, _to, _tokenId);
    }

    function getApproved(uint256 _tokenId) public view returns (address) {
        require(_owners[_tokenId] != address(0), "ERC721: invalid token ID");
        return _tokenApprovals[_tokenId];
    }

    function isApprovedForAll(address _owner, address _operator) public view returns (bool) {
        return _operatorApprovals[_owner][_operator];
    }
}
"""

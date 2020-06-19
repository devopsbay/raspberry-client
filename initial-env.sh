#!/usr/bin/env bash

export MASTER_KEYS='["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]'
export DOORS="[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]},{\"name\":\"101\",\"pin_id\":20,\"readers\":[\"D22\",\"D27\"]}]"
export READER_TIMEOUT="0.5"
export HUB_HOST="https://dev.panel.lesnahub.pl"
export CLIENT_ID="1"
export NFC_READER_MODULE="nfcclient.nfc_reader.nfc_reader.NFCReaderImpl"
export DOOR_OPEN_SECONDS="1"

{
    env | grep MASTER_KEYS;
    env | grep DOORS;
    env | grep READER_TIMEOUT;
    env | grep HUB_HOST;
    env | grep CLIENT_ID;
    env | grep NFC_READER_MODULE;
    env | grep DOOR_OPEN_SECONDS;
} > .env
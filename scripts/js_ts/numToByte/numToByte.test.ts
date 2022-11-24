import * as assert from 'assert'
import numToByte from './index'

describe("ConvertNumberToByteArray", function () {
  describe("It should be `['01', '2c']`", () => {
    assert.deepEqual(numToByte(300, 16), ['01', '2c'])
  })
})
// =====================================================================================================================
// Modern Control Map (The Witcher 3) - the behaviour the controller map needs that bindings alone cannot give. Every part
// acts only on a controller and only when the binding it serves is in place, so a player with other bindings gets the
// game's own handlers. Wrappers over events: no early return.
//   1. Sprint: out of combat a tap toggles running, a hold runs while held.
//   2. Swords: Draw Steel and Draw Silver on one button - a tap does the steel sword, a hold the silver one.
//   3. Dismount: the hold-to-dismount circle follows Horse Dismount's own button (the game hands it a fixed B).
//   4. Sign buttons: with alternative sign casting on, the game's Select Aard ... Select Axii cast only while Cast Sign is
//      held; the casts the game hangs on Sprint, the attacks and Witcher Senses are not made; Jump waits.
// =====================================================================================================================

// the first pad button the game has for an action, or IK_None
function MCM_FirstPadKey(action : name) : EInputKey
{
	var keys : array<EInputKey>;
	var i : int;

	theInput.GetPadKeysForAction(action, keys);
	for (i = 0; i < keys.Size(); i += 1)
	{
		if (keys[i] != IK_None)
		{
			return keys[i];
		}
	}
	return IK_None;
}

function MCM_AltSignHeld() : bool
{
	if (!thePlayer || !thePlayer.GetInputHandler())
	{
		return false;
	}
	return thePlayer.GetInputHandler().GetIsAltSignCastingPressed();
}

// ---- 1. Sprint: tap toggles, hold runs (out of combat, controller) --------------------------------------------------
// The game's own Sprint Toggle answers a pad only with its Left Stick Sprint option on, and that option makes the Sprint
// button itself do nothing - so the toggle is the game's own SetSprintToggle, called on a quick release of Sprint.

@addField(CPlayerInput)
var mcmSprintPressedAt : float;

@wrapMethod(CPlayerInput)
function OnCommSprint(action : SInputAction)
{
	var now : float;

	if (theInput.LastUsedGamepad())
	{
		now = theGame.GetEngineTimeAsSeconds();
		if (IsPressed(action))
		{
			mcmSprintPressedAt = now;
		}
		else if (IsReleased(action) && mcmSprintPressedAt > 0)
		{
			if (now - mcmSprintPressedAt <= 0.2f && thePlayer && thePlayer.IsAlive() && !thePlayer.IsInCombat()
				&& !GetIsAltSignCastingPressed())
			{
				thePlayer.SetSprintToggle(!thePlayer.GetIsSprintToggled());
			}
			mcmSprintPressedAt = 0;
		}
	}
	wrappedMethod(action);
}

// ---- 2. Swords on one button ----------------------------------------------------------------------------------------
// Each the game's own draw (EBAT_Draw_Steel / EBAT_Draw_Silver -> OnEquipMeleeWeapon with "sheathe if already equipped"):
// nothing drawn -> draw; that sword drawn -> sheathe; the other sword drawn -> switch. The hold acts on release.

@addField(CPlayerInput)
var mcmSwordPressedAt : float;

function MCM_SwordsOnOneButton() : bool
{
	var steel : EInputKey;

	if (!theInput.LastUsedGamepad())
	{
		return false;
	}
	steel = MCM_FirstPadKey('SteelSword');
	return steel != IK_None && steel == MCM_FirstPadKey('SilverSword');
}

function MCM_DrawOrSheathe(silver : bool)
{
	if (thePlayer.IsActionAllowed(EIAB_DrawWeapon) && thePlayer.GetBIsInputAllowed() && thePlayer.GetWeaponHolster().IsMeleeWeaponReady())
	{
		if (silver)
		{
			thePlayer.PushCombatActionOnBuffer(EBAT_Draw_Silver, BS_Pressed);
		}
		else
		{
			thePlayer.PushCombatActionOnBuffer(EBAT_Draw_Steel, BS_Pressed);
		}
		if (thePlayer.GetBIsCombatActionAllowed())
		{
			thePlayer.ProcessCombatActionBuffer();
		}
	}
	else if (!thePlayer.IsActionAllowed(EIAB_DrawWeapon))
	{
		thePlayer.DisplayActionDisallowedHudMessage(EIAB_DrawWeapon);
	}
}

@wrapMethod(CPlayerInput)
function OnCommSteelSword(action : SInputAction)
{
	var now : float;

	// while Cast Sign is held on a controller the button is a sign's own (Yrden on X): no sword
	if (!(theInput.LastUsedGamepad() && GetIsAltSignCastingPressed()))
	{
		if (MCM_SwordsOnOneButton())
		{
			now = theGame.GetEngineTimeAsSeconds();
			if (IsPressed(action))
			{
				mcmSwordPressedAt = now;
			}
			else if (IsReleased(action) && mcmSwordPressedAt > 0)
			{
				MCM_DrawOrSheathe(now - mcmSwordPressedAt >= 0.3f);
				mcmSwordPressedAt = 0;
			}
		}
		else
		{
			wrappedMethod(action);
		}
	}
}

@wrapMethod(CPlayerInput)
function OnCommSilverSword(action : SInputAction)
{
	// with both swords on one button, the silver sword is the steel handler's hold - this press is that same press
	if (!MCM_SwordsOnOneButton() && !(theInput.LastUsedGamepad() && GetIsAltSignCastingPressed()))
	{
		wrappedMethod(action);
	}
}

// ---- 3. Dismount follows its binding --------------------------------------------------------------------------------
// The horse state and the GUI manager give the hold-to-dismount indicator a fixed IK_Pad_B_CIRCLE, and a completed hold
// on it dismounts - with Gallop on B, holding B threw the rider off. The indicator gets Horse Dismount's own pad button.

@wrapMethod(CR4GuiManager)
function EnableHudHoldIndicator_Impl(gpadKeyCode : int, kbKeyCode : int, label : string, holdDuration : float, optional intName : name)
{
	var dismountKey : EInputKey;

	if (intName == 'HorseDismount' && gpadKeyCode == (int)IK_Pad_B_CIRCLE)
	{
		dismountKey = MCM_FirstPadKey('HorseDismount');
		if (dismountKey != IK_None)
		{
			gpadKeyCode = (int)dismountKey;
		}
	}
	wrappedMethod(gpadKeyCode, kbKeyCode, label, holdDuration, intName);
}

// ---- 4. Sign buttons ------------------------------------------------------------------------------------------------

// set while OnSelectSign runs, so AltCastSign knows the cast came from a sign's own button
@addField(CPlayerInput)
var mcmCastFromSignButton : bool;

// when a sign was last cast from its own button on a pad (engine seconds)
@addField(CPlayerInput)
var mcmSignButtonCastAt : float;

function MCM_JumpHeldBack() : bool
{
	if (!thePlayer || !thePlayer.GetInputHandler() || !theInput.LastUsedGamepad())
	{
		return false;
	}
	return MCM_AltSignHeld() || theGame.GetEngineTimeAsSeconds() - thePlayer.GetInputHandler().mcmSignButtonCastAt < 0.5f;
}

@wrapMethod(CPlayerInput)
function OnSelectSign(action : SInputAction)
{
	// on a controller a sign's own button only casts while Cast Sign is held; on its own it does nothing
	if (!(theInput.LastUsedGamepad() && IsPressed(action) && !GetIsAltSignCastingPressed()))
	{
		if (IsPressed(action) && theInput.LastUsedGamepad())
		{
			mcmSignButtonCastAt = theGame.GetEngineTimeAsSeconds();
		}
		mcmCastFromSignButton = true;
		wrappedMethod(action);
		mcmCastFromSignButton = false;
	}
}

@wrapMethod(CPlayerInput)
function AltCastSign(signType : ESignType)
{
	if (mcmCastFromSignButton || !theInput.LastUsedGamepad() || !MCM_SignButtonsBound())
	{
		wrappedMethod(signType);
	}
}

// the sign buttons are in use when the player has given Select Igni a pad button (the installer does)
function MCM_SignButtonsBound() : bool
{
	return MCM_FirstPadKey('SelectIgni') != IK_None;
}

@wrapMethod(CExplorationInput)
function IsJumpPressedInTime() : bool
{
	if (MCM_JumpHeldBack())
	{
		return false;
	}
	return wrappedMethod();
}

@wrapMethod(CExplorationInput)
function IsJumpJustPressed() : bool
{
	if (MCM_JumpHeldBack())
	{
		return false;
	}
	return wrappedMethod();
}

@wrapMethod(CExplorationInput)
function IsJumpPressed() : bool
{
	if (MCM_JumpHeldBack())
	{
		return false;
	}
	return wrappedMethod();
}
